#include <SFML/Graphics.hpp>
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
#include <stack>
#include <math.h>

struct Node:sf::RectangleShape{
    int x;
    int y;
    bool isWall = false;
    bool visited = false;
    float fLocalGoal;
    float fGlobalGoal;
    std::vector<Node*> vecNeighbor;
    Node* parent;
};

struct CompareDistance {
    bool operator()(Node const* p1, Node const* p2)
    {
        // return "true" if "p1" is ordered
        // before "p2", for example:
        return p1->fGlobalGoal > p2->fGlobalGoal;
    }
};

float vectorDistance(Node* a, Node* b) {
    return sqrt((b->x - a->x) * (b->x - a->x) + (b->y - a->y) * (b->y - a->y));
}

void printList(Node* node) {
    Node* p = node;

    while (p->parent != nullptr) {
        std::cout << p->x << " " << p->y << " ";
        p = p->parent;
    }
    std::cout << std::endl;
}


void aStar(Node* startNode, Node* endNode, Node* nodes, int gridWidth, int gridHeight) {
    //reset graph
    for (int i = 0; i < gridWidth; i++) {
        for (int j = 0; j < gridHeight; j++) {
            nodes[j * gridWidth + i].visited = false;
            nodes[j * gridWidth + i].parent = nullptr;
            nodes[j * gridWidth + i].fGlobalGoal = INFINITY;
            nodes[j * gridWidth + i].fLocalGoal = INFINITY;
        }
    }

    startNode->fLocalGoal = 0;
    startNode->fGlobalGoal = vectorDistance(startNode, endNode);
    std::priority_queue<Node*, std::vector<Node*>, CompareDistance> pq;

    pq.push(startNode);

    while (!pq.empty()) {
        Node* node = pq.top();
        pq.pop();
        if (node == endNode)
            continue;
        for (auto n : node->vecNeighbor) {
            float d = vectorDistance(node, n);
            if (!n->visited && !n->isWall) {
                if (node->fLocalGoal + d < n->fLocalGoal) {
                    n->fLocalGoal = node->fLocalGoal + d;
                    n->fGlobalGoal = vectorDistance(n, endNode) + n->fLocalGoal;
                    n->parent = node;

                    pq.push(n);
                }
            }
        }
        node->visited = true;
    }

}

void bfs(Node* startNode, Node* endNode, Node* nodes, int gridWidth, int gridHeight) {
    //reset graph
    for (int i = 0; i < gridWidth; i++) {
        for (int j = 0; j < gridHeight; j++) {
            nodes[j * gridWidth + i].visited = false;
            nodes[j * gridWidth + i].parent = nullptr;
            nodes[j * gridWidth + i].fGlobalGoal = INFINITY;
            nodes[j * gridWidth + i].fLocalGoal = INFINITY;
        }
    }

    std::queue<Node*> q;

    q.push(startNode);

    while (!q.empty()) {
        Node* node = q.front();

        q.pop();
        if (node == endNode)
            break;
        for (auto n : node->vecNeighbor) {
            float d = vectorDistance(node, n);
            if (!n->visited && !n->isWall) {
                n->parent = node;
                q.push(n);
            }
        }
        node->visited = true;
    }
}

void dfs(Node* startNode, Node* endNode, Node* nodes, int gridWidth, int gridHeight) {
    //reset graph
    for (int i = 0; i < gridWidth; i++) {
        for (int j = 0; j < gridHeight; j++) {
            nodes[j * gridWidth + i].visited = false;
            nodes[j * gridWidth + i].parent = nullptr;
            nodes[j * gridWidth + i].fGlobalGoal = INFINITY;
            nodes[j * gridWidth + i].fLocalGoal = INFINITY;
        }
    }

    std::stack<Node*> s;

    s.push(startNode);

    while (!s.empty()) {
        Node* node = s.top();

        s.pop();
        if (node == endNode)
            break;
        for (auto n : node->vecNeighbor) {
            float d = vectorDistance(node, n);
            if (!n->visited && !n->isWall) {
                n->parent = node;
                s.push(n);
            }
        }
        node->visited = true;
    }
}


int main()
{
    const int W = 1000;
    const int H = 1000;
    Node* nodes = nullptr;
    Node* startNode = nullptr;
    Node* endNode = nullptr;
    int gridWidth = 15;
    int gridHeight = 15;
    double n = gridWidth * gridHeight;
    double px = ceil(sqrt(n * W / H));
    double sx, sy;
    
    if (floor((px * H / W)) * px < n)
        sx = H / ceil(px * H / W);
    else
        sx = W / px;

    double py = ceil(sqrt(n * H / W));

    if (floor(py * W / H) * py < n)
        sy = W / ceil(W * py / H);
    else
        sy = H / py;

    int maxSide = std::max(sx, sy);
    int borderSize = 10;

    int xpos = 10;
    int ypos = 10;

    sf::RenderWindow window(sf::VideoMode(W + 10, H + 10), "Pathfinding Program");
    window.setFramerateLimit(60);

    nodes = new Node[gridWidth * gridHeight];

    for (int i = 0; i < gridWidth; i++) {
        for (int j = 0; j < gridHeight; j++) {
            nodes[j * gridWidth + i].x = xpos;
            nodes[j * gridWidth + i].y = ypos;
            nodes[j * gridWidth + i].isWall = false;
            nodes[j * gridWidth + i].parent = nullptr;
            nodes[j * gridWidth + i].setPosition(sf::Vector2f(xpos, ypos));
            nodes[j * gridWidth + i].setFillColor(sf::Color(0, 0, 225));
            //nodes[j * gridWidth + i].setOutlineThickness(borderSize);
            //nodes[j * gridWidth + i].setOutlineColor(sf::Color(random, 0, 0));
            nodes[j * gridWidth + i].setSize(sf::Vector2f(maxSide - borderSize, maxSide - borderSize));
            ypos += maxSide;
        }
        xpos += maxSide;
        ypos = 10;
    }
    //start and end nodes
    startNode = &nodes[(gridHeight / 2) * gridWidth + 1];
    endNode = &nodes[(gridHeight / 2) * gridWidth + (gridWidth - 2)];

    for (int i = 0; i < gridWidth; i++) {
        for (int j = 0; j < gridHeight; j++) {
            //get north neighbor
            if (j > 0)
                nodes[j * gridWidth + i].vecNeighbor.push_back(&nodes[(j - 1) * gridWidth + i]);
            //get south neighbor
            if (j < gridHeight - 1)
                nodes[j * gridWidth + i].vecNeighbor.push_back(&nodes[(j + 1) * gridWidth + i]);
            //get east neighbor
            if (i < gridWidth - 1)
                nodes[j * gridWidth + i].vecNeighbor.push_back(&nodes[j * gridWidth + (i + 1)]);
            //get west neighbor
            if (i > 0)
                nodes[j * gridWidth + i].vecNeighbor.push_back(&nodes[j * gridWidth + (i - 1)]);
        }
    }

    while (window.isOpen())
    {

        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Escape))
                window.close();
            if (event.type == sf::Event::MouseButtonPressed) {
                int x = sf::Mouse::getPosition(window).x;
                int y = sf::Mouse::getPosition(window).y;

                for (int i = 0; i < gridWidth; i++) {
                    for (int j = 0; j < gridHeight; j++) {
                        int nodex = nodes[j * gridWidth + i].x;
                        int nodey = nodes[j * gridWidth + i].y;

                        if ((x >= nodex && x <= nodex + maxSide - borderSize) && (y >= nodey && y <= nodey + maxSide - borderSize)) {
                            nodes[j * gridWidth + i].isWall = !nodes[j * gridWidth + i].isWall;
                        }
                    }
                }

                dfs(startNode, endNode, nodes, gridWidth, gridHeight);
            }
        }

        //render
        window.clear();
        
        for (int i = 0; i < gridWidth; i++) {
            for (int j = 0; j < gridHeight; j++) {
                for (auto n : nodes[j * gridWidth + i].vecNeighbor) {
                    sf::Vertex line[] =
                    {
                        sf::Vertex(sf::Vector2f(nodes[j * gridWidth + i].x + (maxSide / 2), nodes[j * gridWidth + i].y + (maxSide / 2))),
                        sf::Vertex(sf::Vector2f(n->x + (maxSide / 2), n->y + (maxSide / 2) ))
                    };
                    line[0].color = sf::Color::Blue;
                    line[1].color = sf::Color::Blue;
                    window.draw(line, 2, sf::Lines);
                }
            }
        }
        
        for (int i = 0; i < gridWidth; i++) {
            for (int j = 0; j < gridHeight; j++) {
                if (nodes[j * gridWidth + i].isWall)
                    nodes[j * gridWidth + i].setFillColor(sf::Color(220, 220, 220));
                else {
                    if(nodes[j* gridWidth + i].visited)
                        nodes[j * gridWidth + i].setFillColor(sf::Color(0, 0, 145));
                    else
                        nodes[j * gridWidth + i].setFillColor(sf::Color(0, 0, 225));
                }

                if (&nodes[j * gridWidth + i] == startNode)
                    nodes[j * gridWidth + i].setFillColor(sf::Color::Green);
                if (&nodes[j * gridWidth + i] == endNode)
                    nodes[j * gridWidth + i].setFillColor(sf::Color::Red);
                window.draw(nodes[j * gridWidth + i]);
            }
        }

        if (endNode != nullptr) {
            Node* p = endNode;
            while (p->parent != nullptr) {
                sf::Vertex line[] =
                {
                    sf::Vertex(sf::Vector2f(p->x + (maxSide / 2), p->y + (maxSide / 2))),
                    sf::Vertex(sf::Vector2f(p->parent->x + (maxSide / 2), p->parent->y + (maxSide / 2)))
                };
                line[0].color = sf::Color::Yellow;
                line[1].color = sf::Color::Yellow;
                window.draw(line, 2, sf::Lines);

                p = p->parent;
            }
        }

        window.display();
    }

    return 0;
}