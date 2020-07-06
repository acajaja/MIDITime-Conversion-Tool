import argparse

class ValidateMidiValue(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         if (values <= 0 or values > 127):
             raise ValueError('MIDI velocities can only be between 1 - 127')
         else:
             setattr(namespace, self.dest, values)