import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # get a list of all the pages
    all_pages = []
    for key in corpus:
        all_pages.append(key)

    # get a list of all the pages the current page links to
    linked_pages = corpus[page]

    # if page has no links, return probability distribution that chooses at random from all pages
    if len(linked_pages) == 0:
        transition_dictionary = {}
        all_page_probability = (float(100) / len(all_pages)) / 100

        for element in all_pages:
            transition_dictionary[element] = all_page_probability

        return transition_dictionary
            
    # calculate probability with damping
    linked_page_probability = damping_factor * ((float(100) / len(linked_pages)) / 100)

    # calculate probability with 1 - damping
    all_page_probability = (1 - damping_factor) * ((float(100) / len(all_pages)) / 100)

    # create the dictionary
    transition_dictionary = {}
    for element in linked_pages:
        transition_dictionary[element] = linked_page_probability + all_page_probability

    for element in all_pages:
        if element not in transition_dictionary:
            transition_dictionary[element] = all_page_probability

    return transition_dictionary


    



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a list of all the pages
    all_pages = []
    for key in corpus:
        all_pages.append(key)

    # Choose a page at random
    random_index = random.randint(0, len(all_pages) - 1)
    sampling_page = all_pages[random_index]
    all_samples = []


    while n != 0:
        n = n - 1
        transition_blueprint = transition_model(corpus, sampling_page, damping_factor)
        weights = []
        for value in transition_blueprint.values():
            weights.append(value)

        all_pages = []
        for key in transition_blueprint.keys():
            all_pages.append(key)

        sample = random.choices(
            population= all_pages,
            weights= weights
        )
        all_samples.append(sample[0])
        sampling_page = sample[0]

    sample_amount = len(all_samples)
    page_rank = {}
    for page in all_pages:
        total_count = 0
        for sample in all_samples:
            if page == sample:
                total_count = total_count + 1

        page_rank[page] = total_count / sample_amount

    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # get a list of all the pages
    all_pages = []
    page_rank = {}
    for page in corpus:
        all_pages.append(page)

    for page in all_pages:
        page_rank[page] = 1 / float(len(all_pages))

    print("page_rank before: ", page_rank)
    
    times_repeated = 0
    #?##########################################################################################################
    #? a page that has no links at all should be treated as if having links to all other pages, including itself
    for values in corpus.values():
        if len(values) == 0:
            for page in all_pages:
                values.add(page)
    #?##########################################################################################################
    print("Corpus: ", corpus)


    for page in page_rank:
        page_rank_formula_first = float((1 - damping_factor)) / len(all_pages)
        print("page rank formula first ", page_rank_formula_first)
        page_rank_formula_second = 0

        # get a list of all pages that link to the page
        all_pages_that_link = []
        # go over every page and see if it links to the original page
        for a_page in all_pages:
            if page in corpus[a_page]:
                all_pages_that_link.append(a_page)

        
        # iterate over every page that links to the original page
        for linking_page in all_pages_that_link:
            page_rank_formula_second = page_rank_formula_second + (float(page_rank[linking_page]) / len(corpus[linking_page]))

        page_rank_formula_second = page_rank_formula_second * damping_factor 

        page_rank[page] = page_rank_formula_first + page_rank_formula_second

    print("page rank after: ", page_rank)
    sum_check = 0
    for value in page_rank.values():
        print(value)
        sum_check = sum_check + value

    print("Sum check: ", sum_check)

    



if __name__ == "__main__":
    main()
