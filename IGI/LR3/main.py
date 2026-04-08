"""
Purpose: Main module to run all tasks.
"""
import utils, init_logic
import task1, task2, task3, task4, task5

def main():
    while True:
        print("\n--- Menu ---")
        print("1-5: Tasks | 0: Exit")
        choice = utils.get_int("Choice: ")
        
        if choice == 1:
            x = utils.get_float("x (-1 < x < 1): ")
            e = utils.get_float("eps: ")
            res = task1.calculate_arcsin(x, e)
            if res:
                print(f"| x: {x} | n: {res[1]} | F(x): {res[0]:.6f} | Math: {res[2]:.6f} |")
        
        elif choice == 2:
            print(f"Max: {task2.find_max_sequence()}")
            
        elif choice == 3:
            t = input("Text: ")
            print(f"Count: {task3.count_non_spaces(t)}")
            
        elif choice == 4:
            up, low, zw, zi, txt = task4.analyze_alice()
            print(f"Upper: {up}, Lower: {low}, Z-word: {zw}, Filtered: {txt[:50]}...")
            
        elif choice == 5:
            size = utils.get_int("Size: ")
            print("1: Manual | 2: Random")
            m = utils.get_int("> ")
            gen = init_logic.user_input_generator(size) if m == 1 else init_logic.random_generator(size)
            # Переводим генератор в список для работы с индексами
            lst = list(gen)
            print(f"List: {lst}")
            p, s = task5.process_list(lst)
            print(f"Prod (even): {p}, Sum (zeros): {s}")
            
        elif choice == 0: break
        
        if input("\nAgain? (y/n): ").lower() != 'y': break

if __name__ == "__main__":
    main()