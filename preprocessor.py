""" Data Preprocessor class to preprocess lyrics"""
from typing import List


class Preprocessor():
    def __init__(self):
        """ Class which preprocesses the lyrics
        that were scraped from the website
        
        Parameters
        ----------
        text_preprocessed: List[str]
            The final preprocessed text
        """  
        self.text_preprocessed = []
    
    def run(self, file_path: str) -> None:
        """ 
        Runs the preprocessing pipeline
        
        Parameters
        ----------
        file_path: str
            file to read the data from

        Returns
        -------
        None
        """
        with open(file_path, 'r') as file:
            self.text_preprocessed = self.remove_empty_lines(file.read().split("\n"))
            self.text_preprocessed = self.lower_text(self.text_preprocessed)
            print(self.text_preprocessed[:30])
        self.file_save(file_path)
    
    def remove_empty_lines(self, text: List[str]) -> List[str]:
        """ 
        Remove empty lines from the lyrics
        
        Parameters
        ----------
        text: List[str]
            Lyrics extracted from the file

        Returns
        -------
        List[str]:
            Lyrics without empy lines
        """
        return [line for line in text if line != '']

    def lower_text(self, text: List[str]) -> List[str]:
        """ 
        Lowers the letters
        
        Parameters
        ----------
        text: List[str]
            Lyrics extracted from the file

        Returns
        -------
        List[str]:
            Lyrics with lower case letters only
        """
        return [line.lower() for line in text]

    def file_save(self, file_path: str) -> None:
        """ 
        Saves preprocessed lyrics to new txt file.
        
        Parameters
        ----------
        file_path: str
            path from which the text was read from

        Returns
        -------
        None
        """
        # Change file name to not overwrite the original text
        file_path_save = file_path[:-4] + "_preprocessed" + file_path[-4:]
        with open(file_path_save, 'w') as file:
            # Need to convert list of strings back to a single string
            file.write("\n".join(self.text_preprocessed))


if __name__ == "__main__":
    file_path = "./data/Coldplay.txt"
    preprocessor = Preprocessor()
    preprocessor.run(file_path)