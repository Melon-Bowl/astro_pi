from math import sqrt

from src.metric import MetricController


class AccelerometerController(MetricController):
  """Controller for methods and data related to the accelerometer.
  Inherits from the ``MetricController`` class.

  :param con: Reference to main controller
  :type con: main.Controller
  """
  def __init__(self, con):
    dev = (2 * 3**0.5) * (0.3 if con.testing else 0.05)
    super().__init__(dev, 'accelerometer')
    self.con = con
    self.sense = con.sense

  def measure_value(self):
    values = self.sense.get_accelerometer_raw()
    return (values['x'], values['y'], values['z'])

  def check_deviance(self, new_value: tuple) -> bool:
    """Compares the difference of each direction of the new value to find any deviance
    and then checks the deviance of the vector as a whole.
    For now if the difference is over 25% of the average, then it is a deviant.
    """
    if len(self.history) < 5:
      return False

    else:
      past_value = self.history[-5:]
      past_value_average = 0
      vector_average = 0

      for i in range(3):
        for t in range(5):
          past_value_average += past_value[t][i]
        if abs((new_value[i] - past_value_average / 5) / (past_value_average / 5)) > 0.5:
          return True
        past_value_average = 0

      for a in range(5):
        vector_average += sum(map(lambda x: x**2, past_value[a]))**0.5
      vector_average = (vector_average) / 5
      if abs(sum(map(lambda x: x**2, new_value))**0.5 - vector_average) / vector_average > 0.5:
        return True

      return False
