import subprocess
import sys

def main():
    repo_name = "ai-student-ppt-maker"
    print(f"Creating & pushing repository {repo_name} to GitHub...")
    
    # 1. Check if repo already exists, if not create using gh cli
    res = subprocess.run(["gh", "repo", "view", f"SHIVA-TIWARI2403/{repo_name}"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Repository does not exist yet. Creating public repo SHIVA-TIWARI2403/{repo_name}...")
        create_res = subprocess.run([
            "gh", "repo", "create", f"SHIVA-TIWARI2403/{repo_name}",
            "--public",
            "--description", "🎓 SlideGen AI — Free AI Presentation Maker for Students with Pictures, Animations & Viva Notes",
            "--source=.",
            "--remote=origin",
            "--push"
        ], capture_output=True, text=True)
        print(create_res.stdout)
        if create_res.returncode == 0:
            print(f"Successfully published to https://github.com/SHIVA-TIWARI2403/{repo_name}")
            return
        else:
            print("Notice:", create_res.stderr)

    # If repo exists or remote already set
    subprocess.run(["git", "remote", "add", "origin", f"https://github.com/SHIVA-TIWARI2403/{repo_name}.git"], capture_output=True)
    push_res = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True)
    print(push_res.stdout)
    if push_res.returncode == 0:
        print(f"Successfully pushed updates to https://github.com/SHIVA-TIWARI2403/{repo_name}")
    else:
        print("Push output:", push_res.stderr)

if __name__ == "__main__":
    main()
