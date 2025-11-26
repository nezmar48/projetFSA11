import optimize
import simulation
import tracker
import pressure

def quit():
    print("Quitting")
    raise SystemExit

def main():
    commands = {
        "quit": quit,
        "sims": simulation.sims,
        "v0" : optimize.find_v0_shell,
        "c" : optimize.find_c_shell,
        "tracker" : tracker.tracker_shell,
        "test" : pressure.test
    }

    print("Simple shell. Type a command:")
    while True:
        cmd = input("> ").strip().lower()
        if cmd in commands:
            commands[cmd]()
        else:
            print("Unknown command. Available:", ", ".join(commands))

if __name__ == "__main__":
    main()
