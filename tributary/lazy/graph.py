from .node import Node
from ..base import TributaryException


class LazyGraph(object):
    """Wrapper class around a collection of lazy nodes."""

    def __init__(self, *args, **kwargs):
        # the last thing we do is go through all of our methods and ensure that all `_callable_args` in our methods are replaced with nodes
        for meth in dir(self):
            meth = getattr(self, meth)

            # bind self on nodes
            if isinstance(meth, Node):
                meth._self_reference = self

            elif hasattr(meth, "_node_wrapper"):
                node = meth._node_wrapper
                if node is None:
                    continue
                # FIXME redo
                # modify in place in case used elsewhere
                # for i, arg in enumerate(node._callable_args):
                #     if not isinstance(arg, Node):
                #         replace = getattr(self, arg)
                #         if not isinstance(replace, Node) and (
                #             isinstance(replace, types.FunctionType)
                #             or isinstance(replace, types.MethodType)
                #         ):
                #             # call function to get node
                #             replace = replace()
                #         node._callable_args[i] = replace

                # # modify in place in case used elsewhere
                # for k, arg in node._callable_kwargs.items():
                #     if not isinstance(arg, Node):
                #         replace = getattr(self, arg)
                #         if not isinstance(replace, Node) and (
                #             isinstance(replace, types.FunctionType)
                #             or isinstance(replace, types.MethodType)
                #         ):
                #             # call function to get node
                #             replace = replace()
                #         node._callable_kwargs[k] = replace

    def node(self, name, readonly=False, nullable=True, value=None):  # noqa: F811
        """method to create a lazy node attached to a graph.

        Args:
            name (str): name to represent the node
            readonly (bool): whether the node should be settable
            nullable (bool): whether node can have value None
            value (any): initial value for node
        Returns:
            BaseNode: the newly constructed lazy node
        """
        if not hasattr(self, "_LazyGraph__nodes"):
            self.__nodes = {}

        if name not in self.__nodes:
            if not isinstance(value, Node):
                value = Node(
                    name=name,
                    value=value,
                )
            self.__nodes[name] = value
            setattr(self, name, self.__nodes[name])
        return self.__nodes[name]

    def __getattribute__(self, name):
        if name == "_LazyGraph__nodes" or name == "__nodes":
            return super(LazyGraph, self).__getattribute__(name)
        elif hasattr(self, "_LazyGraph__nodes") and name in super(
            LazyGraph, self
        ).__getattribute__("_LazyGraph__nodes"):
            return super(LazyGraph, self).__getattribute__("_LazyGraph__nodes")[name]
        else:
            return super(LazyGraph, self).__getattribute__(name)

    def __setattr__(self, name, value):
        if hasattr(self, "_LazyGraph__nodes") and name in super(
            LazyGraph, self
        ).__getattribute__("_LazyGraph__nodes"):
            node = super(LazyGraph, self).__getattribute__("_LazyGraph__nodes")[name]
            if isinstance(value, Node) and node == value:
                return
            elif isinstance(value, Node):
                raise TributaryException("Cannot set to node")
            else:
                node.setValue(value)
        else:
            super(LazyGraph, self).__setattr__(name, value)
