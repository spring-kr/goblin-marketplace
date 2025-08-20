from stem_integration_new import STEMIntegration
import json


def main():
    s = STEMIntegration()
    ip = "127.0.0.1"
    results = []
    results.append(s.process_question("assistant", "업무 효율을 높이는 방법을 알려줘", ip))
    results.append(s.process_question("assistant", "좀 더 구체적으로 단계별 방법 알려줘", ip))
    with open("chat_smoke_test_output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("WROTE chat_smoke_test_output.json", len(results))


if __name__ == "__main__":
    main()
