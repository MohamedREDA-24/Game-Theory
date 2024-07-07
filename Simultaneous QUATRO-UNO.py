import tkinter as tk
from tkinter import messagebox

class SimultaneousQuatroUnoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simultaneous QUATRO-UNO")
        
        self.cards = [1, 2, 3, 4]
        self.ann_pile = []
        self.beth_pile = []

        self.ann_wins = 0
        self.beth_wins = 0
        self.draws = 0

        self.create_widgets()

    def create_widgets(self):
        # Frame for card selection
        self.selection_frame = tk.Frame(self.root)
        self.selection_frame.pack(pady=10)

        # Ann's card selection
        self.ann_label = tk.Label(self.selection_frame, text="Ann's Card Selection:")
        self.ann_label.grid(row=0, column=0, padx=10)
        self.ann_buttons = []
        for i in range(1, 5):
            button = tk.Button(self.selection_frame, text=str(i), command=lambda idx=i: self.select_card('Ann', idx))
            button.grid(row=0, column=i, padx=5)
            self.ann_buttons.append(button)

        # Beth's card selection
        self.beth_label = tk.Label(self.selection_frame, text="Beth's Card Selection:")
        self.beth_label.grid(row=1, column=0, padx=10)
        self.beth_buttons = []
        for i in range(1, 5):
            button = tk.Button(self.selection_frame, text=str(i), command=lambda idx=i: self.select_card('Beth', idx))
            button.grid(row=1, column=i, padx=5)
            self.beth_buttons.append(button)

        # Button to start the game
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        # Button to play again
        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again)
        self.play_again_button.pack(pady=5)
        self.play_again_button.config(state=tk.DISABLED)

        # Label to display game results
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        # Label to display Ann's wins
        self.ann_wins_label = tk.Label(self.root, text=f"Ann's Wins: {self.ann_wins}")
        self.ann_wins_label.pack()

        # Label to display Beth's wins
        self.beth_wins_label = tk.Label(self.root, text=f"Beth's Wins: {self.beth_wins}")
        self.beth_wins_label.pack()

        # Label to display draws
        self.draws_label = tk.Label(self.root, text=f"Draws: {self.draws}")
        self.draws_label.pack()

        # Frame for payoff matrix
        self.payoff_frame = tk.Frame(self.root)
        self.payoff_frame.pack(pady=10)

        # Label for payoff matrix
        self.payoff_label = tk.Label(self.payoff_frame, text="Payoff Matrix:")
        self.payoff_label.grid(row=0, column=0, padx=10)

        # Text widget to display payoff matrix
        self.payoff_text = tk.Text(self.payoff_frame, height=15, width=60)
        self.payoff_text.grid(row=1, column=0, padx=10)

    def select_card(self, player, card):
        if player == 'Ann':
            if len(self.ann_pile) < 4:
                self.ann_pile.append(card)
                self.ann_buttons[card-1].config(state=tk.DISABLED)
        elif player == 'Beth':
            if len(self.beth_pile) < 4:
                self.beth_pile.append(card)
                self.beth_buttons[card-1].config(state=tk.DISABLED)

    def start_game(self):
        if len(self.ann_pile) != 4 or len(self.beth_pile) != 4:
            messagebox.showerror("Error", "Both Ann and Beth must select 4 cards.")
            return
        
        self.game = SimultaneousQuatroUno()
        result = self.game.play_game(self.ann_pile.copy(), self.beth_pile.copy())

        self.generate_payoff_matrix()


        self.result_label.config(text=result)


        if result == "Ann wins!":
            self.ann_wins += 1
        elif result == "Beth wins!":
            self.beth_wins += 1
        else:
            self.draws += 1


        self.ann_wins_label.config(text=f"Ann's Wins: {self.ann_wins}")
        self.beth_wins_label.config(text=f"Beth's Wins: {self.beth_wins}")
        self.draws_label.config(text=f"Draws: {self.draws}")


        self.play_again_button.config(state=tk.NORMAL)

        self.reset_card_selection()

    def play_again(self):
        self.ann_pile = []
        self.beth_pile = []
        self.result_label.config(text="")
        self.generate_payoff_matrix()
        self.reset_card_selection()

        self.play_again_button.config(state=tk.DISABLED)

    def generate_payoff_matrix(self):
        matrix = []
        for ann_card in self.ann_pile:
            row = []
            for beth_card in self.beth_pile:
                result = self.game.play_round(ann_card, beth_card)
                # if result == 'Ann':
                #     row.append('Ann wins')
                # elif result == 'Beth':
                #     row.append('Beth wins')
                # else:
                #     row.append('Draw')
                if result == 'Ann':
                    row.append('3,0')
                elif result == 'Beth':
                    row.append('0,3')
                else:
                    row.append('2,2')
            matrix.append(row)



        self.payoff_text.delete(1.0, tk.END)
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                self.payoff_text.insert(tk.END, f'{cell}\t\t')
            self.payoff_text.insert(tk.END, '\n')

    def reset_card_selection(self):
        for button in self.ann_buttons:
            button.config(state=tk.NORMAL)
        for button in self.beth_buttons:
            button.config(state=tk.NORMAL)


class SimultaneousQuatroUno:
    def __init__(self):
        self.cards = [1, 2, 3, 4]
        self.ann_card = None
        self.beth_card = None

    def play_round(self, ann_card, beth_card):
        self.ann_card = ann_card
        self.beth_card = beth_card
        if ann_card == beth_card:
            return None  
        elif ann_card == 1 and beth_card == 4:
            return None  
        elif ann_card == 4 and beth_card == 1:
            return None
        elif ann_card > beth_card:
            return 'Ann'
        else:
            return 'Beth'

    def play_game(self, ann_pile, beth_pile):
        while ann_pile and beth_pile:
            p1_number = ann_pile[0]
            p2_number = beth_pile[0]

            if p1_number == 1 and p2_number == 4:
                ann_pile.pop(0)
                beth_pile.pop(0)
            elif p2_number == 1 and p1_number == 4:
                ann_pile.pop(0)
                beth_pile.pop(0)
                
            elif p1_number > p2_number:
                beth_pile.pop(0)
            elif p1_number < p2_number:
                ann_pile.pop(0)
            else:
                ann_pile.pop(0)
                beth_pile.pop(0)

        if not ann_pile and not beth_pile:
            return "It's a draw!"
        elif not ann_pile:
            return "Beth wins!"
        else:
            return "Ann wins!"


def main():
    root = tk.Tk()
    app = SimultaneousQuatroUnoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
