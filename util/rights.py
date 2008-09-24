# rights.py
#
# support for privileges according to GENI specification

# privilege_table:
#
# a list of priviliges and what operations are allowed per privilege

privilege_table = {"authority": ["*"],
                   "refresh": ["remove", "update"],
                   "resolve": ["resolve", "list", "getcredential"],
                   "sa": ["*"],
                   "embed": ["getticket", "createslice", "deleteslice", "updateslice"],
                   "bind": ["getticket", "loanresources"],
                   "control": ["updateslice", "stopslice", "startslice", "deleteslice", "resetslice"],
                   "info": ["listslices", "listcomponentresources", "getsliceresources"],
                   "ma": ["*"]}

# a "Right" is a single privilege.

class Right:
   def __init__(self, kind):
      self.kind = kind

   def can_perform(self, op_name):
      allowed_ops = privilege_table.get(self.kind.lower(), None)
      if not allowed_ops:
         return False

      # if "*" is specified, then all ops are permitted
      if "*" in allowed_ops:
         return True

      return (op_name.lower() in allowed_ops)

   def is_superset(self, child):
      my_allowed_ops = privilege_table.get(self.kind.lower(), None)
      child_allowed_ops = privilege_table.get(child.kind.lower(), None)

      if "*" in my_allowed_ops:
          return True

      for right in child_allowed_ops:
          if not right in my_allowed_ops:
              return False

      return True

# a "RightList" is a list of privileges

class RightList:
    def __init__(self, string=None):
        self.rights = []
        if string:
            self.load_from_string(string)

    def add(self, right):
        if isinstance(right, str):
            right = Right(kind = right)
        self.rights.append(right)

    def load_from_string(self, string):
        self.rights = []

        # none == no rights, so leave the list empty
        if not string:
            return

        parts = string.split(",")
        for part in parts:
            self.rights.append(Right(part))

    def save_to_string(self):
        right_names = []
        for right in self.rights:
            right_names.append(right.kind)

        return ",".join(right_names)

    def can_perform(self, op_name):
        for right in self.rights:
            if right.can_perform(op_name):
                return True
        return False

    def is_superset(self, child):
        for child_right in child.rights:
            allowed = False
            for my_right in self.rights:
                if my_right.is_superset(child_right):
                    allowed = True
            if not allowed:
                return False
        return True

