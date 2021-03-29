from evennia import Command


class CmdPoke(Command):
    """
    Pokes someone.

    Usage: poke <target>
    """
    key = "poke"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        if len(self.args) == 0:
            self.caller.msg("Poke what?")
            return
        target = self.caller.search(self.args.lstrip())
        if not target:
            return
        if self.caller == target:
            self.caller.msg("You poke yourself.")
            return
        target.msg(f"{self.caller} pokes you.")
        self.caller.msg(f"You poke {target}.")