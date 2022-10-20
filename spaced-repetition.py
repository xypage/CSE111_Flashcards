dict = {
  "problem_id": [
    [2.5], # Current effort factor, defaults to 2.5 for new items
    [0] # previous spacings, start with a 0 so new terms come quickly
  ]
}

# Using https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
# Effort factor is calculated each time you answer correctly, and helps determine how long till the next interval
# I = which iteration this is, increments by 1 every time you get it right
# q is quality of answer, where 5 = perfect, 4 = correct w/hesitation, 3 = correct w/difficulty,
#   2 = wrong but quickly remember when shown, 1 = wrong and recognize correct answer, 0 = no recollection
def get_interval(problem_id, q):
  (EFs, spacings) = dict[problem_id]

  # An effort factor needs to be calculated, regardless of whether they answered it right or wrong
  # EF':= EF+(0.1-(5-q)*(0.08+(5-q)*0.02))
  new_EF = EFs[-1] + (0.1-(5-q)*(0.08+(5-q)*0.02))
  # We want to lock it between 1.3 and 2.5, just to make sure it's not going to be too often or too rare
  if(new_EF < 1.3):
    new_EF = 1.3
  if(new_EF > 2.5):
    new_EF = 2.5
  EFs.append(new_EF)

  # If they got it wrong, you want to drop spacings all the way back no matter what
  if q < 3:
    spacings = 1
    return

  # Otherwise, you follow the formula
  # I(1):=1
  # I(2):=6
  # I(n>2):=I(n-1)*EF
  i = len(spacings)
  if(i == 1):
    spacings.append(1)
  elif(i == 2):
    spacings.append(6)
  else:
    spacings.append(spacings[-1] * new_EF)