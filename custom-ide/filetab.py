from tkinter import Frame
from tkinter.constants import END

class FileTab(Frame):
    variables = list()
    funcs = list()


    def __init__(self, root) -> None:
        super().__init__(root)
        self.textwidget = None
        print("Created a new tab!")

    def getAllWords(self) -> list:
        words = self.textwidget.get("1.0", END)
        words = str(words).split()
        return words

    def getAllVariables(self) -> list:
        """
        You would want to use this comaped to 
        {\n
            tab = FileTab(root)

            variables = tab.variables
        }\n
        Because it doesnt loop through it everytime.
        """
        words = self.getAllWords()

        for i in range(len(words) - 1):
            if words[i + 1] == "=":
                self.variables.append((words[i], words[i + 2]))

        return self.variables

    def getAllFunctions(self) -> list:
        """
        You would want to use this comaped to 
        {\n
            tab = FileTab(root)

            functions = tab.functions
        }\n
        Because it doesnt loop through it everytime.
        """
        words = self.getAllWords()
        
        for i in range(len(words)):
            if words[i] == "def":
                self.funcs.append((words[i], words[i + 1]))
        
        return self.funcs
