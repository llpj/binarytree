from heapq import heapify
from random import sample, random

_node_init_func = None
_node_cls = None
_null = None
_left_attr = 'left'
_right_attr = 'right'
_value_attr = 'value'


class Node(object):
    """Represents a binary tree node."""

    def __init__(self, value):
        self.__setattr__(_value_attr, value)
        self.__setattr__(_left_attr, _null)
        self.__setattr__(_right_attr, _null)

    def __repr__(self):
        return 'Node({})'.format(self.__getattribute__(_value_attr))


def _new_node(value):
    if _node_init_func is not None:
        return _node_init_func(value)
    return (_node_cls or Node)(value)


def _is_list(obj):
    return isinstance(obj, list)


def _is_node(obj):
    return isinstance(obj, _node_cls or Node)


def _value_of(node):
    return getattr(node, _value_attr)


def _left_of(node):
    return getattr(node, _left_attr)


def _right_of(node):
    return getattr(node, _right_attr)


def _add_left(parent, child):
    setattr(parent, _left_attr, child)


def _add_right(parent, child):
    setattr(parent, _right_attr, child)


def _is_balanced(node):
    """Return depth if balanced else -1."""
    if node == _null:
        return 0

    left = _is_balanced(_left_of(node))
    right = _is_balanced(_right_of(node))

    if left < 0 or right < 0 or abs(left - right) > 1:
        return -1
    return max(left, right) + 1


def _build_list(root):
    """Build a list of values from a tree."""
    result = []
    current_nodes = [root]
    level_not_empty = True

    while level_not_empty:
        level_not_empty = False
        next_nodes = []

        for node in current_nodes:
            if node == _null:
                result.append(_null)
                next_nodes.append(_null)
                next_nodes.append(_null)
            else:
                result.append(_value_of(node))

                left_child = _left_of(node)
                right_child = _right_of(node)

                if left_child != _null:
                    level_not_empty = True
                if right_child != _null:
                    level_not_empty = True

                next_nodes.append(left_child)
                next_nodes.append(right_child)

        current_nodes = next_nodes

    while result and result[-1] == _null:
        result.pop()
    return result


def _build_tree(values):
    """Build a tree from a list of values."""
    if not values:
        return _null

    nodes = [_null for _ in values]
    if values[0] == _null:
        raise ValueError('Node missing at index 0')

    root = _new_node(values[0])
    nodes[0] = root

    index = 1
    while index < len(values):
        value = values[index]
        if value != _null:
            parent_index = int((index + 1) / 2) - 1
            parent_node = nodes[parent_index]
            if parent_node == _null:
                raise ValueError(
                    'Node missing at index {}'
                    .format(parent_index)
                )
            child_node = _new_node(value)
            if index % 2:  # is odd
                _add_left(parent_node, child_node)
            else:
                _add_right(parent_node, child_node)
            nodes[index] = child_node
        index += 1

    return root


def _build_str(node):
    """Helper function used for display."""
    if node == _null:
        return 0, 0, 0, []

    line1 = []
    line2 = []
    val_len = gap_len = len(str(_value_of(node)))

    l_len, l_val_from, l_val_to, l_lines = _build_str(_left_of(node))
    r_len, r_val_from, r_val_to, r_lines = _build_str(_right_of(node))

    if l_len > 0:
        l_anchor = -int(-(l_val_from + l_val_to) / 2) + 1  # ceiling
        line1.append(' ' * (l_anchor + 1))
        line1.append('_' * (l_len - l_anchor))
        line2.append(' ' * l_anchor + '/')
        line2.append(' ' * (l_len - l_anchor))
        val_from = l_len + 1
        gap_len += 1
    else:
        val_from = 0

    line1.append(str(_value_of(node)))
    line2.append(' ' * val_len)

    if r_len > 0:
        r_anchor = int((r_val_from + r_val_to) / 2)  # floor
        line1.append('_' * r_anchor)
        line1.append(' ' * (r_len - r_anchor + 1))
        line2.append(' ' * r_anchor + '\\')
        line2.append(' ' * (r_len - r_anchor))
        gap_len += 1
    val_to = val_from + val_len - 1

    gap = ' ' * gap_len
    lines = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_lines), len(r_lines))):
        l_line = l_lines[i] if i < len(l_lines) else ' ' * l_len
        r_line = r_lines[i] if i < len(r_lines) else ' ' * r_len
        lines.append(l_line + gap + r_line)

    return len(lines[0]), val_from, val_to, lines


def _bst_insert(root, value):
    """Insert a node into the BST."""
    depth = 1
    node = root
    while True:
        if _value_of(node) > value:
            left_child = _left_of(node)
            if left_child == _null:
                _add_left(node, _new_node(value))
                break
            node = left_child
        else:
            right_child = _right_of(node)
            if right_child == _null:
                _add_right(node, _new_node(value))
                break
            node = right_child
        depth += 1
    return depth


def _random_insert(root, value):
    """Insert a node randomly into the tree."""
    depth = 1
    node = root
    while True:
        if random() < 0.5:
            left_child = _left_of(node)
            if left_child == _null:
                _add_left(node, _new_node(value))
                break
            node = left_child
        else:
            right_child = _right_of(node)
            if right_child == _null:
                _add_right(node, _new_node(value))
                break
            node = right_child
        depth += 1
    return depth


def _validate_tree(root):
    """Check if the tree is malformed.

    Each node in the tree must be of the specified class (default: Node) and
    not have a null value (default: None).

    :param root: the binary tree node
    :type root: binarytree.Node
    :return:
    """
    current_nodes = [root]

    while current_nodes:
        next_nodes = []
        for node in current_nodes:
            if _is_node(node):
                if _value_of(node) == _null:
                    raise ValueError('A node cannot have a null value')
                next_nodes.append(_left_of(node))
                next_nodes.append(_right_of(node))
            elif node != _null:
                # Halt if the node is not NULL nor a node instance
                raise ValueError('Found an invalid node in the tree')
        current_nodes = next_nodes


def _generate_values(height, multiplier=1):
    if not isinstance(height, int) or height < 0:
        raise ValueError('Height must be a non-negative integer')
    count = 2 ** (height + 1) - 1
    return sample(range(count * multiplier), count)


def setup(node_class=Node,
          node_init_func=None,
          null_value=None,
          value_attr='value',
          left_attr='left',
          right_attr='right'):
    """Setup a custom definition of the binary tree node.

    :param node_class: the tree node class
    :type node_class: object
    :param node_init_func: node initializer function
    :type node_init_func:

    :param null_value: the null value to signify "no child" (default: None)
    :type null_value: object
    :param value_attr: the value attribute (default: "value")
    :type right_attr: str
    :param left_attr: the left child attribute (default: "left")
    :type left_attr: str
    :param right_attr: the right child attribute (default: "right")
    :type right_attr: str
    """
    global _node_cls
    global _node_init_func
    global _null
    global _value_attr
    global _left_attr
    global _right_attr

    _node_cls = node_class
    _node_init_func = node_init_func
    _null = null_value
    _value_attr = value_attr
    _left_attr = left_attr
    _right_attr = right_attr


def tree(height=4, balanced=False):
    values = _generate_values(height)
    if balanced:
        return _build_tree(values)

    root = _new_node(values[0])
    for index in range(1, len(values)):
        depth = _random_insert(root, values[index])
        if depth == height:
            break
    return root


def bst(height=4):
    values = _generate_values(height)
    root = _new_node(values[0])
    for index in range(1, len(values)):
        depth = _bst_insert(root, values[index])
        if depth == height:
            break
    return root


def heap(height=4, max=False):
    values = _generate_values(height)
    if max:
        negated = [-v for v in values]
        heapify(negated)
        return _build_tree([-v for v in negated])
    else:
        heapify(values)
        return _build_tree(values)


def pprint(bt):
    """Pretty print the binary tree.

    :param bt: the binary tree to display
    :raises ValueError: if an invalid tree is given
    """
    if bt == _null:
        return
    if _is_list(bt):
        if not bt:
            return
        bt = _build_tree(bt)
    elif _is_node(bt):
        _validate_tree(bt)
    else:
        raise ValueError('Expecting a list or a node')
    print('\n' + '\n'.join(_build_str(bt)[-1]))


def convert(bt):
    """Convert a binary tree into a list, or list into a binary tree.

    :param bt: the binary tree to convert
    :return: the converted form of the binary tree
    :raises ValueError: if an invalid tree is given
    """
    if bt == _null:
        return []
    if _is_list(bt):
        return _build_tree(bt)
    elif _is_node(bt):
        _validate_tree(bt)
        return _build_list(bt)
    raise ValueError('Expecting a list or a node')


def inspect(bt):
    """Return the properties of the binary tree.

    :param bt: the binary tree to inspect
    :return: the properties of the binary tree
    :raises ValueError: if an invalid tree is given
    """
    if _is_list(bt):
        bt = _build_tree(bt)
    elif _is_node(bt):
        _validate_tree(bt)
    else:
        raise ValueError('Expecting a list or a node')

    is_bst = True
    is_descending = True
    is_ascending = True
    is_left_padded = True
    min_value = float('inf')
    max_value = float('-inf')
    node_count = 0
    leaf_count = 0
    min_leaf_depth = 0
    current_depth = -1
    current_nodes = [bt]

    while current_nodes:

        null_encountered = False
        current_depth += 1
        next_nodes = []

        for node in current_nodes:
            node_count += 1
            node_value = _value_of(node)
            min_value = min(node_value, min_value)
            max_value = max(node_value, max_value)

            left_child = _left_of(node)
            right_child = _right_of(node)

            for child in (left_child, right_child):
                if child != _null and null_encountered:
                    is_left_padded = False
                elif child == _null and not null_encountered:
                    null_encountered = True

            if left_child == _null and right_child == _null:
                if min_leaf_depth == 0:
                    min_leaf_depth = current_depth
                leaf_count += 1

            if left_child != _null:
                if _value_of(left_child) > node_value:
                    is_descending = False
                    is_bst = False
                elif _value_of(left_child) < node_value:
                    is_ascending = False
                next_nodes.append(left_child)

            if right_child != _null:
                if _value_of(right_child) > node_value:
                    is_descending = False
                elif _value_of(right_child) < node_value:
                    is_ascending = False
                    is_bst = False
                next_nodes.append(right_child)

        current_nodes = next_nodes

    is_balanced = _is_balanced(bt) >= 0

    return {
        'is_height_balanced': current_depth - min_leaf_depth < 2,
        'is_weight_balanced': is_balanced,
        'is_max_heap': is_descending and is_left_padded and is_balanced,
        'is_min_heap': is_ascending and is_left_padded and is_balanced,
        'is_bst': is_bst,
        'height': current_depth,
        'leaf_count': leaf_count,
        'node_count': node_count,
        'min_leaf_depth': min_leaf_depth,
        'max_leaf_depth': current_depth,
        'min_value': min_value,
        'max_value': max_value
    }
