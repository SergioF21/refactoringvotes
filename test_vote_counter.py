# test_vote_counter.py
import csv
from io import StringIO

import unittest
from unittest.mock import patch, mock_open
from vote_counter import count_votes,separationOfARow,addingVotes  # Assuming starter version is in `vote_counter.py`

class TestVoteCounter(unittest.TestCase):

    @patch("builtins.print")
    def test_count_votes_valid_file(self, mock_print):
        mock_csv = """city,candidate,votes
        Springfield,Alice,1200
        Springfield,Bob,750
        Shelbyville,Alice,2000
        Shelbyville,Bob,2500"""
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            count_votes("votes.csv")
        
        # Expected output after tallying votes
        mock_print.assert_any_call("Alice: 3200 votes")
        mock_print.assert_any_call("Bob: 3250 votes")
        mock_print.assert_any_call("winner is Bob")
        self.assertEqual(mock_print.call_count, 3)

    @patch("builtins.print")
    def test_count_votes_invalid_votes(self, mock_print):
        # Simulate a CSV file with invalid votes data
        mock_csv = """city,candidate,votes
        Springfield,Bob,750
        Shelbyville,Alice,2000
        Springfield,Alice,invalid
        Shelbyville,Bob,2500"""
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            count_votes("votes.csv")

        # Expect Alice to be skipped due to invalid data, only Bob's votes should print correctly
        mock_print.assert_any_call("Bob: 3250 votes")
        mock_print.assert_any_call("Alice: 2000 votes")
        mock_print.assert_any_call("winner is Bob")
        self.assertEqual(mock_print.call_count, 3)

    def test_tie_case(self):
        # Datos de prueba con empate entre "Alice" y "Bob"
        test_data = StringIO("City,Candidate,Votes\nCityA,Alice,100\nCityB,Bob,100\n")
        # Función simulada de count_votes que lee de test_data en lugar de un archivo
        def count_votes_from_data(data):
            results = {}
            reader = csv.reader(data, delimiter=',')
            next(reader)  # Omitir el encabezado
            
            for row in reader:
                city, candidate, votes = separationOfARow(row)
                addingVotes(candidate, results, votes)
                
            # Verificación del empate
            sorted_by_votes = sorted(results.items(), key=lambda item: item[1], reverse=True)
            self.assertEqual(sorted_by_votes[0][1], sorted_by_votes[1][1], "It should be a draw")

            # Verificación de que uno de los candidatos empatados sea el ganador
            winner = sorted_by_votes[0][0]
            self.assertIn(winner, ["Alice", "Bob"], "The winner should be one of the tied candidates")

        # Ejecutar la prueba
        count_votes_from_data(test_data)

if __name__ == "__main__":
    unittest.main()

