import unittest
import pandas as pd
from src.graph import Graph

class TestGraphMethods(unittest.TestCase):

    def setUp(self):
        # Créez une instance de la classe Graph pour les tests
        self.graph = Graph()

    def test_add_drug(self):
        # Testez l'ajout d'un médicament à la graph
        drug_row = pd.Series({'atccode': 'A01', 'drug': 'Aspirin'})
        self.graph.add_drug(drug_row)
        self.assertTrue('drug_A01' in self.graph.G.nodes)

    def test_add_pubmed(self):
        # Testez l'ajout d'un article PubMed à la graph
        pubmed_row = pd.Series({'id': 1, 'title': 'Study on Aspirin', 'journal': 'Medical Journal'})
        self.graph.add_pubmed(pubmed_row)
        self.assertTrue('pubmed_1' in self.graph.G.nodes)
        self.assertTrue('journal_Medical Journal' in self.graph.G.nodes)

    def test_add_clinical_trial(self):
        # Testez l'ajout d'un essai clinique à la graph
        trial_row = pd.Series({'id': 1, 'scientific_title': 'Clinical Trial with Aspirin', 'journal': 'Clinical Journal'})
        self.graph.add_clinical_trial(trial_row)
        self.assertTrue('clinical_trial_1' in self.graph.G.nodes)
        self.assertTrue('journal_Clinical Journal' in self.graph.G.nodes)

    def test_get_drugs_of_journal(self):
        # Testez la récupération des médicaments d'un journal donné
        drug_row = pd.Series({'atccode': 'A01', 'drug': 'Aspirin'})
        pubmed_row = pd.Series({'id': 1, 'title': 'Study on Aspirin', 'journal': 'Medical Journal'})
        self.graph.add_drug(drug_row)
        self.graph.add_pubmed(pubmed_row)
        drugs_of_journal = self.graph.get_drugs_of_journal('journal_Medical Journal')
        self.assertEqual(drugs_of_journal, ['drug_A01'])

    def test_get_journal_with_most_drugs(self):
        # Testez la récupération du journal avec le plus de médicaments
        drug_row1 = pd.Series({'atccode': 'A01', 'drug': 'Aspirin'})
        drug_row2 = pd.Series({'atccode': 'B01', 'drug': 'Ibuprofen'})
        pubmed_row1 = pd.Series({'id': 1, 'title': 'Study on Aspirin', 'journal': 'Medical Journal'})
        pubmed_row2 = pd.Series({'id': 2, 'title': 'Ibuprofen Study', 'journal': 'Medical Journal'})
        self.graph.add_drug(drug_row1)
        self.graph.add_drug(drug_row2)
        self.graph.add_pubmed(pubmed_row1)
        self.graph.add_pubmed(pubmed_row2)
        journals_with_most_drugs = self.graph.get_journal_with_most_drugs()
        self.assertEqual(journals_with_most_drugs, ['journal_Medical Journal'])

if __name__ == '__main__':
    unittest.main()
