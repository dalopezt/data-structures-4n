#include <cmath>
#include <iostream>
#include <fstream>
#include <vector>

class Node
{
    private:
    int _value;
    Node* _left;
    Node* _right;
    int _height;

    public:
    Node(int value)
    {
        _value = value;
        _left = nullptr;
        _right = nullptr;
        _height = 1;
    }

    int get_value() { return _value; }
    int get_height() { return _height; }
    Node* get_left() { return _left; }
    Node* get_right() { return _right; }

    void set_height(int height) { _height = height; }
    void set_left(Node* left) { _left = left; }
    void set_right(Node* right) { _right = right; }
};

class AVLTree
{
    private:
    Node* _root;

    int get_node_height(Node* node)
    {
        if (!node) return 0;
        return node->get_height();
    }

    int compute_node_balance(Node* node)
    {
        if (!node) return 0;
        return 
              get_node_height(node->get_left()) 
            - get_node_height(node->get_right());
    }

    int recompute_height(Node* node)
    {
        return 1 + 
            __max(
                get_node_height(node->get_left()), 
                get_node_height(node->get_right()));
    }

    Node* insert(Node* root, int value)
    {
        if (!root)
        {
            Node* aux = new Node(value);
            return aux;
        } 
        else if (value < root->get_value()) 
            root->set_left(
                insert(root->get_left(), value));
        else
            root->set_right(
                insert(root->get_right(), value));
        
        root->set_height(
            recompute_height(root));
        int balance = compute_node_balance(root);

        // LL
        if (balance > 1 && value < root->get_left()->get_value())
            return right_rotate(root);

        // RR
        if (balance < -1 && value > root->get_right()->get_value())
            return left_rotate(root);
        
        // LR
        if (balance > 1 && value > root->get_left()->get_value())
        {
            root->set_left(left_rotate(root->get_left()));
            return right_rotate(root);
        }   
        
        // RL
        if (balance < -1 && value < root->get_right()->get_value())
        {
            root->set_right(left_rotate(root->get_right()));
            return left_rotate(root);
        }
        
        return root;
    }

    Node* left_rotate(Node* root)
    {
        Node* aux = root->get_right();
        root->set_right(aux->get_left());
        aux->set_left(root);

        root->set_height(recompute_height(root));
        aux->set_height(recompute_height(aux));

        return aux;
    }

    Node* right_rotate(Node* root)
    {
        Node* aux = root->get_left();
        root->set_left(aux->get_right());
        aux->set_right(root);

        root->set_height(recompute_height(root));
        aux->set_height(recompute_height(aux));

        return aux;
    }


    public:
    Node* get_root() { return _root; }

    void insert_value(int value)
    {
        _root = insert(_root, value);
    }

    void inorder(Node* node)
    {
        if (node)
        {
            inorder(node->get_left());
            std::cout << "{v: " << node->get_value() << ", h: " << node->get_height() << "}\n";
            inorder(node->get_right());
        }
    }

    int tree_size(Node* node)
    {
        if (!node) return 0;
        return tree_size(node->get_left())
               + 1
               + tree_size(node->get_right());
    }

    std::vector<int> get_nodes_value(Node* node)
    {
        std::vector<int> r;
        
        // If null, doesn't add anything
        if (!node) return r;

        // Insert left edges
        std::vector<int> left_nodes = get_nodes_value(node->get_left());
        r.insert(
            r.end(), 
            left_nodes.begin(), 
            left_nodes.end());

        // Add itself
        r.push_back(node->get_value());

        // Insert right edges
        std::vector<int> right_nodes = get_nodes_value(node->get_right());
        r.insert(
            r.end(), 
            right_nodes.begin(), 
            right_nodes.end());

        return r;
    }

    std::vector<std::pair<int, int>> get_edges(Node* node)
    {
        std::vector<std::pair<int, int>> r;
        
        // If null, doesn't add anything
        if (!node) return r;

        // Insert left edges
        std::vector<std::pair<int, int>> left_edges = get_edges(node->get_left());
        r.insert(
            r.end(), 
            left_edges.begin(), 
            left_edges.end());
        
        // Insert self edges
        if (node->get_left())
        {
            std::pair<int, int> left;
            left.first = node->get_value();
            left.second = node->get_left()->get_value();
            r.push_back(left);
        }
        if (node->get_right())
        {
            std::pair<int, int> right;
            right.first = node->get_value();
            right.second = node->get_right()->get_value();
            r.push_back(right);
        }

        // Insert right edges
        std::vector<std::pair<int, int>> right_edges = get_edges(node->get_right());
        r.insert(
            r.end(), 
            right_edges.begin(), 
            right_edges.end());
        
        return r;
    }

    void save()
    {
        std::ofstream file("avl.txt");
        
        std::vector<int> nodes = get_nodes_value(_root);
        file << _root->get_value() << "\n";
        file << "[";
        for (auto node : nodes)
        {
            file << node;
            if (node == nodes.back()) file << "]\n";
            else file << ", ";
        }
        
        std::vector<std::pair<int, int>> edges = get_edges(_root);
        for (auto edge : edges)
        {
            file << "(" << edge.first << ", " << edge.second << ")\n";
        }

        file.close();
    }
};

int main(void)
{
    AVLTree tree;
    int n;
    int m;
    std::cout << "Number of nodes: ";
    std::cin >> n;
    for (int i = 0; i < n; ++i)
    {
        std::cout<< "Value of " << i+1 << " node: ";
        std::cin >> m;
        tree.insert_value(m);
    }
    tree.inorder(tree.get_root());
    tree.save();
}