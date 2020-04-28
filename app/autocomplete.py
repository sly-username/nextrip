# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from collections import defaultdict

#import time
#start_time = time.time()

## launch url
url = 'https://www.metro.net/riding/nextrip/bus-arrivals/'

## create a new Firefox session
driver = webdriver.Firefox()
#driver.implicitly_wait(30)
driver.get(url)
driver.switch_to.frame(0)

## select bus stop information
route = Select(driver.find_element_by_name('routeSelector'))
direction = Select(driver.find_element_by_name('directionSelector'))
stop = Select(driver.find_element_by_name('stopSelector'))

routes = []
for option in route.options:
    routes.append(option.text.strip())

directions = []
for option in direction.options:
    directions.append(option.text.strip())
    
stops = []
for option in stops.options:
    stops.append(option.text.strip())
    
    
#directions = [x for x in direction.find_elements_by_tag_name('select')]




class AutoCompleter(object):
    
    def __init__(self, choices_list):
        self.choices_list = choices_list
        self.token_to_choice_name, self.n_gram_to_tokens = self._create_tokens_database()

    def _create_tokens_database(self):
        token_to_choice_name = defaultdict(list)
        n_gram_to_tokens = defaultdict(set)
        for choice in self.choices_list:
            choice = choice.lower().replace('-', ' ').replace('(', ' ').replace(')', ' ').replace("'", ' ')
            tokens = choice.split()
            for token in tokens:
                token_to_choice_name[token].append(choice)
                for string_size in range(3, len(token) + 1):
                    n_gram = token[:string_size]
                    n_gram_to_tokens[n_gram].add(token)
        #print(token_to_choice_name, n_gram_to_tokens)
        return token_to_choice_name, n_gram_to_tokens

    def _get_real_tokens_from_possible_n_grams(self, tokens):
        real_tokens = []
        for token in tokens:
            token_set = set(self.n_gram_to_tokens[token])
            #token_set = self.n_gram_to_tokens.get(token, set())
            real_tokens.extend(list(token_set))
        return real_tokens

    def _get_scored_choices_uncollapsed(self, real_tokens):
        choices_scores = []
        for token in real_tokens:
            possible_choices = set(self.token_to_choice_name[token])
            for choice in possible_choices:
                score = float(len(token)) / len(choice.replace(' ', ''))
                choices_scores.append((choice, score))
        return choices_scores

    def _combined_choice_scores(self, choices_scores, num_tokens):
        collapsed_choice_to_score = defaultdict(int)
        collapsed_choice_to_occurence = defaultdict(int)
        for choice, score in choices_scores:
            collapsed_choice_to_score[choice] += score
            collapsed_choice_to_occurence[choice] += 1
        for choice in collapsed_choice_to_score.keys():
            collapsed_choice_to_score[choice] *= collapsed_choice_to_occurence[choice] / float(num_tokens)
        return collapsed_choice_to_score

    def _filtered_results(self, choices_scores):
        min_results = 3
        max_results = 10
        score_threshold = 0.4
        max_possibles = choices_scores[:max_results]
        if choices_scores and choices_scores[0][1] == 1.0:
            return [choices_scores[0][0]]

        possibles_within_thresh = [tuple_obj for tuple_obj in choices_scores 
                                   if tuple_obj[1] >= score_threshold]
        min_possibles = possibles_within_thresh if len(possibles_within_thresh) > min_results else max_possibles[:min_results]
        return [tuple_obj[0] for tuple_obj in min_possibles]

    def guess_choices(self, tokens):
        real_tokens = self._get_real_tokens_from_possible_n_grams(tokens)
        choices_scores = self._get_scored_choices_uncollapsed(real_tokens)
        collapsed_choice_to_score = self._combined_choice_scores(choices_scores, len(tokens))
        choices_scores = collapsed_choice_to_score.items()
        choices_scores = sorted(choices_scores, reverse=True)
        return self._filtered_results(choices_scores)


#results = AutoCompleter(routes).guess_choices(['704'])
#print(results)


#start_time = time.time()
#print("--- %s seconds ---" % (time.time() - start_time)) 

## end the Selenium browser session
driver.quit()
