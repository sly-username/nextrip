# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

import re
from collections import defaultdict

import pandas as pd
from tabulate import tabulate
import os


#launch url
url = "https://www.metro.net/riding/nextrip/bus-arrivals/"

# create a new Firefox session
driver = webdriver.Firefox()
#driver.implicitly_wait(30)
driver.get(url)
driver.switch_to.frame(0)

# select bus stop information
route = Select(driver.find_element_by_name('routeSelector'))
direction = Select(driver.find_element_by_name('directionSelector'))
stop = Select(driver.find_element_by_name('stopSelector'))

routes = [x for x in route.find_elements_by_tag_name('option')]
directions = [x for x in direction.find_elements_by_tag_name('option')]
stops = [x for x in stop.find_elements_by_tag_name('option')]




class AutoCompleter(object):
    
    def __init__(self, choices_list):
        self.choices_list = choices_list
        self.tokens, self.token_to_choice_name, self.n_gram_to_tokens = self._create_tokens_datastructure()
        self.real_tokens = self._get_real_tokens_from_possible_n_grams()
        self.choices_scores = self._get_scored_choices_uncollapsed()
        self.collapsed_choice_to_score = self._combined_choice_scores()

    MIN_N_GRAM_SIZE = 3

    def _create_tokens_datastructure(self):
        token_to_choice_name = defaultdict(list)
        n_gram_to_tokens = defaultdict(set)
        for choice in self.choices_list:
            choice = choice.lower().replace("-", " ").replace("(", " ").replace(")", " ").replace("'", " ")
            tokens = choice.split()
            for token in tokens:
                token_to_choice_name[token].append(choice)
                for string_size in xrange(MIN_N_GRAM_SIZE, len(token) + 1):
                    n_gram = token[:string_size]
                    n_gram_to_tokens[n_gram].add(token)
        return tokens, token_to_choice_name, n_gram_to_tokens

    def _get_real_tokens_from_possible_n_grams(self):
        real_tokens = []
        for token in self.tokens:
            token_set = self.n_gram_to_tokens.get(token, set())
            real_tokens.extend(list(token_set))
        return real_tokens

    def _get_scored_choices_uncollapsed(self, real_tokens):
        choices_scores = []
        for token in real_tokens:
            possible_choices = self.token_to_choice_name.get(token, [])
            for choice in possible_choices:
                score = float(len(token)) / len(choice.replace(" ", ""))
                choices_scores.append((choice, score))
        return choices_scores

    def _combined_choice_scores(self, num_tokens):
        collapsed_choice_to_score = defaultdict(int)
        collapsed_choice_to_occurence = defaultdict(int)
        for choice, score in self.choices_scores:
            collapsed_choice_to_score[choice] += score
            collapsed_choice_to_occurence[choice] += 1
        for choice in collapsed_choice_to_score.keys():
            collapsed_choice_to_score[choice] *= collapsed_choice_to_occurence[choice] / float(num_tokens)
        return collapsed_choice_to_score

    def _filtered_results(self):
        min_results = 3
        max_results = 10
        score_threshold = 0.4
        max_possibles = self.choices_scores[:max_results]
        if self.choices_scores and self.choices_scores[0][1] == 1.0:
            return [self.choices_scores[0][0]]

        possibles_within_thresh = [tuple_obj for tuple_obj in self.choices_scores if tuple_obj[1] >= score_threshold]
        min_possibles = possibles_within_thresh if len(possibles_within_thresh) > min_results else max_possibles[:min_results]
        return [tuple_obj[0] for tuple_obj in min_possibles]

    def guess_choices(self, tokens):
        real_tokens = self._get_real_tokens_from_possible_n_grams(tokens)
        choices_scores = self._get_scored_choices_uncollapsed(real_tokens)
        collapsed_choice_to_score = self._combined_choice_scores(choices_scores, len(tokens))
        choices_scores = collapsed_choice_to_score.items()
        choices_scores.sort(key=lambda t: t[1], reverse=True)
        return self._filtered_results(choices_scores)
































#Selenium hands the page source to Beautiful Soup
driver.switch_to.frame('predictionFrame')
soup = BeautifulSoup(driver.page_source)

def get_predictions():
    # select by value
    route.select_by_value('704')
    direction.select_by_value('704_165_0')
    stop.select_by_value('14424')
    
    

    first = soup.findAll('div', attrs={'class' : 'firstPrediction'})
    first_list = []
    for f in first:
        first_list.append(f.text.strip())
    #print(first_list)
    
    second = soup.findAll('div', attrs={'class' : 'secondaryPredictions'})
    second_list = []
    for s in second:
        second_list.append(s.text.strip())
    #print(second_list)
    
    other = soup.findAll('td', attrs={'class' : 'otherRoutesPredictions'})
    other_list = []
    for o in other:
        other_list.append(o.text.strip())
    #print(other_list)
    
    return first_list, second_list, other_list
