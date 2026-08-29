import sys
sys.path.insert(0, 'D:/Swway/Hackathons/SIH 26/test proj')
from scanner.risk.score import calculate_risk_score
from scanner.recommend import get_recommendation

result = calculate_risk_score(algorithm='RSA', business_criticality='medium', asset_type='algorithm')
print(f'Risk result: {result}')
print(f'Recommendation: {get_recommendation("RSA")}')