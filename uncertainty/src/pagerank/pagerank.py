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
    num_pages = len(corpus)
    distribution = dict()

    links = corpus.get(page, set())

    if links:
        base_probability = (1 - damping_factor) / num_pages
        for candidate in corpus:
            distribution[candidate] = base_probability
        additional_probability = damping_factor / len(links)
        for linked_page in links:
            distribution[linked_page] += additional_probability
    else:
        # No outgoing links: treat as linking to every page in the corpus equally.
        equal_probability = 1 / num_pages
        for candidate in corpus:
            distribution[candidate] = equal_probability

    return distribution

def sample_pagerank(corpus: dict, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_counter = dict.fromkeys(corpus, 0)
    pages = list(corpus)
    current_page = random.choice(pages)
    page_counter[current_page] += 1

    for _ in range(n - 1):
        distrib = transition_model(corpus,current_page,damping_factor)
        current_page = random.choices(list(distrib.keys()),weights=list(distrib.values()),k=1)[0]
        page_counter[current_page] += 1

    for page, counter in page_counter.items():
        page_counter[page] = counter / n
    return page_counter



def iterate_pagerank(corpus: dict, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    convergence = False
    previous_rank = dict.fromkeys(corpus, 1/len(corpus))
    new_rank = dict.fromkeys(corpus, 1/len(corpus))
    page_from_links = {page: [] for page in corpus}
    for linked_page in page_from_links.keys():
        page_from_links[linked_page] = [page for page, to_links in corpus.items() if linked_page in to_links or len(to_links) == 0]
    while not convergence:
        previous_rank = new_rank.copy()
        for page,links in corpus.items():
            base_prob = (1-damping_factor) / len(corpus)
            prob = base_prob
            for linked_page in page_from_links[page]:
                if len(corpus.get(linked_page)) == 0:
                    denominator = len(corpus)
                else:
                    denominator = len(corpus.get(linked_page))
                prob += damping_factor * (previous_rank.get(linked_page) / denominator)
            new_rank[page] = prob
        if all(abs(new_rank[page] - previous_rank[page]) <= 0.001 for page in corpus):
            convergence = True
    return new_rank


if __name__ == "__main__":
    main()
