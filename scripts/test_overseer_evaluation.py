import os
import sys

# Add vault scripts directory to python path
sys.path.append(r"C:\Users\omara\Desktop\vault\Aethelgard Vault\scripts")

from overseer_bridge import evaluate_smart_content

test_cases = [
    # 1. High-Value AI & Deep Learning Study
    {
        "app": "YouTube",
        "title": "ModernBERT Architecture and Non-Autoregressive Decision Models Explained",
        "url": "https://youtube.com/watch?v=xyz123",
        "expected": "productive"
    },
    {
        "app": "Chrome",
        "title": "arXiv:2503.23303v2 Sequence Conversion Trajectories with Reinforcement Learning",
        "url": "https://arxiv.org/abs/2503.23303",
        "expected": "productive"
    },
    # 2. Computer Vision & Robotics
    {
        "app": "YouTube",
        "title": "YOLOv8 Real-Time Multi-Object Tracking with OpenCV and Python Tutorial",
        "url": "https://youtube.com/watch?v=yolo123",
        "expected": "productive"
    },
    {
        "app": "YouTube",
        "title": "Arduino SG90 Servo PWM Control and HW-504 Joystick Wiring Guide",
        "url": "https://youtube.com/watch?v=arduino99",
        "expected": "productive"
    },
    # 3. Speedcubing CFOP Practice
    {
        "app": "YouTube",
        "title": "Full OLL in 10 Days - Recognition & Fingertricks for Sub-15 Solvers",
        "url": "https://youtube.com/watch?v=cubing77",
        "expected": "productive"
    },
    # 4. Pure Brainrot & Doomscrolling on YouTube
    {
        "app": "YouTube",
        "title": "I spent 24 Hours in a haunted mansion challenge (GONE WRONG) #shorts",
        "url": "https://youtube.com/shorts/ghost123",
        "expected": "distraction"
    },
    {
        "app": "YouTube",
        "title": "Skibidi Toilet Episode 70 Full Season Reaction Compilation",
        "url": "https://youtube.com/watch?v=skibidi",
        "expected": "distraction"
    },
    # 5. Social Media Doomscrolling (Instagram / TikTok / Facebook)
    {
        "app": "Instagram",
        "title": "",
        "url": "",
        "expected": "distraction"
    },
    {
        "app": "TikTok",
        "title": "Funny Memes Compilation 2026",
        "url": "",
        "expected": "distraction"
    },
    # 6. Social Media Tech Post Exception (e.g. Reading about AI on Facebook / Twitter)
    {
        "app": "Facebook",
        "title": "Luis Buenaventura: Jev by TypeSafe AI and Laya Open Source Decision Models",
        "url": "https://facebook.com/helloluis/posts/123",
        "expected": "productive"
    },
    # 7. Dedicated Productive Apps
    {
        "app": "Obsidian",
        "title": "Aethelgard Vault - Updating 01 Technical Skills",
        "url": "",
        "expected": "productive"
    },
    {
        "app": "Termux",
        "title": "bash - git push origin main",
        "url": "",
        "expected": "productive"
    },
    # 8. Neutral Utility Apps
    {
        "app": "Clock",
        "title": "",
        "url": "",
        "expected": "utility"
    },
    {
        "app": "Calculator",
        "title": "",
        "url": "",
        "expected": "utility"
    }
]

def run_tests():
    print("=" * 70)
    print("🧪 RUNNING PROJECT OVERSEER SMART EVALUATOR TEST SUITE")
    print("=" * 70)
    
    passed = 0
    for i, tc in enumerate(test_cases, 1):
        res = evaluate_smart_content(tc["app"], tc["title"], tc.get("url", ""))
        verdict = res["verdict"]
        is_pass = (verdict == tc["expected"])
        if is_pass:
            passed += 1
            status_icon = "✅"
        else:
            status_icon = "❌"
            
        print(f"Test {i:02d}: {status_icon} [{verdict.upper()}] (Exp: {tc['expected'].upper()}) | App: '{tc['app']}' | Title: '{tc['title'][:35]}'")
        print(f"         🏷️ Tag: {res['tag']} | 🔢 Score: {res['score']:+.2f} | 🗣️ Voice: \"{res['speak']}\"")
        print("-" * 70)
        
    print(f"\n📊 Test Summary: {passed}/{len(test_cases)} Passed ({(passed/len(test_cases))*100:.1f}%)")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
