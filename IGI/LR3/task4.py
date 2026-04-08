"""
Purpose: Task 4 - Alice text analysis.
"""
from utils import simple_decorator

@simple_decorator
def analyze_alice():
    """Analyzes a specific string without regex."""
    s = ("So she was considering in her own mind, as well as she could, "
         "for the hot day made her feel very sleepy and stupid, whether "
         "the pleasure of making a daisy-chain would be worth the trouble "
         "of getting up and picking the daisies, when suddenly a White "
         "Rabbit with pink eyes ran close by her.")
    
    # a) Upper/Lower
    up = sum(1 for c in s if c.isupper())
    low = sum(1 for c in s if c.islower())
    
    # b) First word with 'z'
    words = s.replace(',', '').split()
    z_word = None
    z_idx = -1
    for i, w in enumerate(words):
        if 'z' in w.lower():
            z_word, z_idx = w, i + 1
            break
            
    # c) Exclude 'a'
    no_a = " ".join([w for w in words if not w.lower().startswith('a')])
    
    return up, low, z_word, z_idx, no_a