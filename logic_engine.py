"""A small propositional knowledge base with forward chaining."""


class KnowledgeBase:
    """Store string facts and Horn-clause-style inference rules."""

    def __init__(self):
        self.facts = set()
        self.rules = []

    def tell_fact(self, fact_string):
        """Add a fact to the knowledge base."""
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        """Add a rule as a (premises, conclusion) tuple."""
        self.rules.append((list(premise_list), conclusion_string))

    def clear_facts(self):
        """Clear facts while retaining the knowledge base's rules."""
        self.facts.clear()

    def forward_chain(self):
        """Infer facts until a full pass over the rules adds nothing."""
        new_facts_added = True

        while new_facts_added:
            new_facts_added = False

            for premises, conclusion in self.rules:
                if conclusion not in self.facts and all(
                    premise in self.facts for premise in premises
                ):
                    self.facts.add(conclusion)
                    new_facts_added = True
