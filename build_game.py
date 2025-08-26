"""
Build script for Dodging Simulator
This script creates an executable file that can be run without Python installed.
"""
import os
import subprocess
import shutil
import sys

def build_executable():
    """Build the game executable using PyInstaller."""
    
    print("🎮 Building Dodging Simulator...")
    print("=" * 50)
    
    # Check if icon exists
    icon_path = "game_icon.ico"
    if not os.path.exists(icon_path):
        print("⚠️  Icon file not found. Creating icon first...")
        subprocess.run([sys.executable, "create_icon.py"])
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # Don't show console window
        "--icon=game_icon.ico",         # Use our custom icon
        "--name=Dodging_Simulator",     # Name of the executable
        "--distpath=./dist",            # Output directory
        "--workpath=./build",           # Temporary build directory
        "--specpath=./",                # Where to put the .spec file
        "game_main.py"                  # Main Python file
    ]
    
    # Add data files (assets and modules)
    data_dirs = ["assets", "Dodging_Simulator"]
    for data_dir in data_dirs:
        if os.path.exists(data_dir):
            cmd.extend(["--add-data", f"{data_dir};{data_dir}"])
    
    print("Running PyInstaller...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        print(f"📁 Executable created at: ./dist/Dodging_Simulator.exe")
        print()
        print("🎉 Your game is ready!")
        print("You can now:")
        print("1. Double-click 'Dodging_Simulator.exe' to play")
        print("2. Share the .exe file with friends")
        print("3. Move it to any Windows computer and it will run")
        print()
        print("💡 Tip: The executable contains everything needed to run the game!")
        
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print("Error output:")
        print(e.stderr)
        print()
        print("💡 Common solutions:")
        print("1. Make sure PyInstaller is installed: pip install pyinstaller")
        print("2. Check that start_screen.py exists and runs correctly")
        print("3. Make sure all dependencies are installed")

def clean_build():
    """Clean up build artifacts."""
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["Dodging_Simulator.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}/")
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"🧹 Cleaned {file_name}")

if __name__ == "__main__":
    print("Dodging Simulator - Build Script")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
    else:
        build_executable()
        
        # Ask if user wants to clean up
        response = input("\n🧹 Clean up build files? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            clean_build()
            print("✨ All clean!")
