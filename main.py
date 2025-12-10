# main.py
# this file provides a shell to lunch the different functions of the program
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
        "sims": simulation.sims, #show graphs of simulations
        "v0" : optimize.find_v0_shell, #find velocity to attaign a distance
        "c" : optimize.find_c_shell, #find the constant of drag
        "tracker" : tracker.tracker_shell, #analyze tracker data
        #"test" : pressure.test #this function was not implemented
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
