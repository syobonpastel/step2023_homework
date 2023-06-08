import sys
import collections


class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)

    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Find the most linked pages.

    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.

    def find_shortest_path(self, start, goal):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        # BFS
        start_id = [id for id, title in self.titles.items()
                    if title == start][0]
        goal_id = [id for id, title in self.titles.items() if title == goal][0]
        id_queue = collections.deque()
        id_queue.append(start_id)
        visited = set()
        visited.add(start_id)
        
        # id とそこまでの最短経路の対応を記録する
        # {id: [id, id, id, ...]}
        path = {}
        path[start_id] = [start_id]
        path_len = 0

        while len(id_queue) > 0:
            # print("count: ", path_len, "id_queue: ", id_queue, "visited: ", visited)
            current_id = id_queue.pop()
            path_len += 1
            for dst in self.links[current_id]:
                if dst not in visited:
                    id_queue.append(dst)
                    visited.add(dst)
                    path[dst] = path[current_id] + [dst]
                    if goal_id in visited:
                        print("Path is found!", [self.titles[id] for id in path[goal_id]])
                        return
        print("Path is not found!")
        return

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass

    # Do something more interesting!!

    def find_something_more_interesting(self):
        # ------------------------#
        # Write your code here!  #
        # ------------------------#
        pass


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("usage: %s pages_file links_file" % sys.argv[0])
    #     exit(1)

    # wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia = Wikipedia("./wikipedia_dataset/pages_small.txt",
                          "./wikipedia_dataset/links_small.txt")
    wikipedia.find_shortest_path("A", "B")
    wikipedia.find_shortest_path("C", "A")
    wikipedia.find_shortest_path("A", "C")
    wikipedia.find_shortest_path("C", "D")
    # wikipedia = Wikipedia("./wikipedia_dataset/pages_medium.txt", "./wikipedia_dataset/links_medium.txt")
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
