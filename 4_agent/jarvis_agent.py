import json
import re
import ollama
from src.tools import *

MODEL_NAME = "jarvis"

TOOL_DISPATCHER = {
    # Web & Busca
    "web_search": web_search,
    "open_browser": open_browser,
    "get_weather": get_weather,
    "check_traffic": check_traffic,
    "get_current_location": get_current_location,
    # Sistema & Hardware
    "system_metrics": system_metrics,
    "get_battery_status": get_battery_status,
    "capture_screen": capture_screen,
    "network_diagnostics": network_diagnostics,
    "lock_workstation": lock_workstation,
    "shutdown_routine": shutdown_routine,
    "clear_console": clear_console,
    "abort_last_action": abort_last_action,
    # Dev & Engenharia
    "git_command": git_command,
    "run_tests": run_tests,
    "fetch_logs": fetch_logs,
    "docker_compose": docker_compose,
    "run_build": run_build,
    "open_terminal": open_terminal,
    "ssh_connect": ssh_connect,
    # Mídia, Apps & Ambiente
    "open_app": open_app,
    "play_track": play_track,
    "media_player": media_player,
    "control_lights": control_lights,
    # Agenda & Horário
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "set_timer": set_timer,
    "set_reminder": set_reminder,
    "calendar_check": calendar_check,
    "calendar_create": calendar_create,
    "calendar_delete": calendar_delete,
    "check_inbox": check_inbox,
}


def sanitize_response(text: str) -> str:
    """Remove artefatos residuais do tokenizer ou tags de sistema."""
    tags_to_strip = [
        r"</sys>",
        r"<\\/sys&gt;",
        r"<\/sys>",
        r"<cutter>",
        r"</cutter>",
        r"<output_cutler.*?>",
        r"</output_cutler.*?>",
    ]
    cleaned = text
    for pattern in tags_to_strip:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def parse_tool_payload(response_text: str) -> dict | None:
    """Detecta e extrai o objeto JSON de chamada de ferramenta, caso exista."""
    try:
        payload = json.loads(response_text.strip())
        if isinstance(payload, dict) and "tool" in payload:
            return payload
    except json.JSONDecodeError:
        # Tenta localizar bloco JSON dentro de texto caso haja preâmbulo
        match = re.search(r"\{.*?\}", response_text, re.DOTALL)
        if match:
            try:
                candidate = json.loads(match.group(0))
                if isinstance(candidate, dict) and "tool" in candidate:
                    return candidate
            except json.JSONDecodeError:
                pass
    return None


def execute_tool(tool_name: str, parameters: dict) -> dict:
    """Executa a ferramenta solicitada com tratamento seguro de exceções."""
    if tool_name not in TOOL_DISPATCHER:
        return {
            "status": "error",
            "message": f"Tool '{tool_name}' is not registered in the system dispatcher.",
        }

    handler = TOOL_DISPATCHER[tool_name]
    try:
        # Chama a função passando os parâmetros desempacotados
        return handler(**parameters)
    except TypeError as e:
        return {
            "status": "error",
            "message": f"Invalid parameters provided for {tool_name}: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Execution failed for {tool_name}: {str(e)}",
        }


def run_jarvis():
    # Contexto inicial do J.A.R.V.I.S.
    chat_history = [
        {
            "role": "system",
            "content": (
                "You are J.A.R.V.I.S. Respond concisely, politely, and directly in British English. "
                "If a request requires a system action, output strictly a JSON object matching the required tool specification. "
                "If no action is required, respond in plain text."
            ),
        }
    ]

    print("=" * 45)
    print("      J.A.R.V.I.S. ONLINE & OPERATIONAL      ")
    print("=" * 45)

    while True:
        try:
            user_input = input("\n>>> ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "shutdown"]:
                print("\nShutting down all operational systems. Good day, sir.")
                break

            # 1. Registra a fala do usuário
            chat_history.append({"role": "user", "content": user_input})

            # 2. Primeira chamada ao modelo
            response = ollama.chat(model=MODEL_NAME, messages=chat_history)
            raw_reply = sanitize_response(response["message"]["content"])

            # 3. Verifica se o modelo acionou uma ferramenta
            tool_call = parse_tool_payload(raw_reply)

            if tool_call:
                tool_name = tool_call.get("tool")
                params = tool_call.get("parameters", {})

                print(f"\n[SYSTEM ACTION]: Invoking '{tool_name}' with {params}")

                # Executa a função Python no mundo real
                result = execute_tool(tool_name, params)

                # Anexa a requisição e a resposta da ferramenta ao contexto
                chat_history.append({"role": "assistant", "content": raw_reply})
                chat_history.append(
                    {
                        "role": "user",
                        "content": f'{{"tool_output": {json.dumps(result)}}}',
                    }
                )

                # Segunda chamada: JARVIS resume o resultado com polidez britânica
                feedback_response = ollama.chat(model=MODEL_NAME, messages=chat_history)
                final_speech = sanitize_response(
                    feedback_response["message"]["content"]
                )

                chat_history.append({"role": "assistant", "content": final_speech})
                print(f"\n{final_speech}")

            else:
                # Conversação direta em texto
                chat_history.append({"role": "assistant", "content": raw_reply})
                print(f"\n{raw_reply}")

        except KeyboardInterrupt:
            print("\nInterrupt signal acknowledged. Standing by, sir.")
            break


if __name__ == "__main__":
    run_jarvis()
