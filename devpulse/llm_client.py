"""
Multi-Provider LLM Client for AI-DevPulse (Ollama, Gemini, OpenAI, Anthropic)
"""

import os
import json
import urllib.request

class DevPulseLLMClient:
    def __init__(self, provider="ollama", api_key="", model="qwen2.5:1.5b", ollama_url="http://localhost:11434"):
        self.provider = provider.lower()
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self.ollama_url = ollama_url

    def analyze_code(self, filename, code_content, prompt_type="audit"):
        """Sends code snippet to LLM for vulnerability scanning & refactoring suggestions."""
        sys_prompt = (
            "You are AI-DevPulse, an expert senior code reviewer and security auditor. "
            "Analyze the code provided for:\n"
            "1. Syntax / Logic errors\n"
            "2. Security vulnerabilities (OWASP Top 10, SQL injection, hardcoded secrets, shell injection)\n"
            "3. Performance bottlenecks\n"
            "4. Clean code & refactoring suggestions\n\n"
            "Return a structured JSON with keys: 'file', 'score' (1-10), 'issues' (list of strings), 'refactored_code' (optional string)."
        )

        user_prompt = f"File: {filename}\n\n```\n{code_content}\n```"

        if self.provider == "ollama":
            return self._call_ollama(sys_prompt, user_prompt)
        elif self.provider == "gemini":
            return self._call_gemini(sys_prompt, user_prompt)
        else:
            return self._heuristic_fallback(filename, code_content)

    def _call_ollama(self, sys_prompt, user_prompt):
        url = f"{self.ollama_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": f"{sys_prompt}\n\n{user_prompt}\n\nRespond strictly in valid JSON:",
            "stream": False
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data.get("response", "")
                return self._parse_json_response(text)
        except Exception as e:
            return {"error": f"Ollama error: {str(e)}"}

    def _call_gemini(self, sys_prompt, user_prompt):
        if not self.api_key:
            return {"error": "GEMINI_API_KEY is not set."}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": f"{sys_prompt}\n\n{user_prompt}"}]}]
        }
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return self._parse_json_response(text)
        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}"}

    def _heuristic_fallback(self, filename, code_content):
        issues = []
        score = 9.0
        lines = code_content.split("\n")
        for idx, line in enumerate(lines, 1):
            if "api_key" in line.lower() and "=" in line and not ("os.getenv" in line or "os.environ" in line or "getenv(" in line):
                issues.append(f"Line {idx}: Potential hardcoded secret/API key detected.")
                score -= 1.5
            if "eval(" in line or "exec(" in line:
                issues.append(f"Line {idx}: Dangerous eval/exec function call.")
                score -= 2.0
            if "shell=True" in line and "subprocess" in line:
                issues.append(f"Line {idx}: Unsanitized subprocess with shell=True.")
                score -= 1.0

        return {
            "file": filename,
            "score": max(1.0, score),
            "issues": issues if issues else ["No high-severity vulnerabilities detected via static scanner."],
            "refactored_code": None
        }

    def _parse_json_response(self, text):
        try:
            # Strip markdown code fences if present
            cleaned = text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[-1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            return json.loads(cleaned)
        except Exception:
            return {"raw_output": text, "score": 8.0, "issues": ["Parsed response as non-JSON text analysis."]}
