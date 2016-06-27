#!/usr/bin/env bash


###
echo "testing ElectreComprehensiveDiscordanceIndex..."
cd ElectreComprehensiveDiscordanceIndex

python ./ElectreComprehensiveDiscordanceIndex.py -i tests/in1 -o tests
diff -s tests/discordance.xml tests/out1/discordance.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/discordance.xml && rm tests/messages.xml
echo "ok"

python ./ElectreComprehensiveDiscordanceIndex.py -i tests/in2 -o tests
diff -s tests/discordance.xml tests/out1/discordance.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/discordance.xml && rm tests/messages.xml
echo "ok"

echo "testing ElectreCrispOutrankingAggregation..."
cd ../ElectreCrispOutrankingAggregation

python ./ElectreCrispOutrankingAggregation.py -i tests/in1 -o tests
diff -s tests/outranking.xml tests/out1/outranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/outranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreCrispOutrankingAggregation.py -i tests/in2 -o tests
diff -s tests/outranking.xml tests/out1/outranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/outranking.xml && rm tests/messages.xml
echo "ok"

echo "testing ElectreDistillation..."
cd ../ElectreDistillation

python ./ElectreDistillation.py -i tests/in1 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in2 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in3 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in4 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in5 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in6 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in7 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in8 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in9 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in10 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillation.py -i tests/in11 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

echo "testing ElectreDistillationRank..."
cd ../ElectreDistillationRank

python ./ElectreDistillationRank.py -i tests/in1 -o tests
diff -s tests/intersection.xml tests/out1/intersection.xml > /dev/null
diff -s tests/median.xml tests/out1/median.xml > /dev/null
diff -s tests/rank.xml tests/out1/rank.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/rank.xml && rm tests/intersection.xml && rm tests/median.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillationRank.py -i tests/in2 -o tests
diff -s tests/intersection.xml tests/out1/intersection.xml > /dev/null
diff -s tests/median.xml tests/out1/median.xml > /dev/null
diff -s tests/rank.xml tests/out1/rank.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/rank.xml && rm tests/intersection.xml && rm tests/median.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillationRank.py -i tests/in3 -o tests
diff -s tests/intersection.xml tests/out1/intersection.xml > /dev/null
diff -s tests/median.xml tests/out1/median.xml > /dev/null
diff -s tests/rank.xml tests/out1/rank.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/rank.xml && rm tests/intersection.xml && rm tests/median.xml && rm tests/messages.xml
echo "ok"

python ./ElectreDistillationRank.py -i tests/in4 -o tests
diff -s tests/intersection.xml tests/out1/intersection.xml > /dev/null
diff -s tests/median.xml tests/out1/median.xml > /dev/null
diff -s tests/rank.xml tests/out1/rank.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/rank.xml && rm tests/intersection.xml && rm tests/median.xml && rm tests/messages.xml
echo "ok"

echo "testing ElectreNFSOutranking..."
cd ../ElectreNFSOutranking

python ./ElectreNFSOutranking.py -i tests/in1 -o tests
diff -s tests/nfs.xml tests/out1/nfs.xml > /dev/null
diff -s tests/strength.xml tests/out1/strength.xml > /dev/null
diff -s tests/weakness.xml tests/out1/weakness.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/nfs.xml && rm tests/strength.xml && rm tests/weakness.xml && rm tests/messages.xml
echo "ok"

python ./ElectreNFSOutranking.py -i tests/in2 -o tests
diff -s tests/nfs.xml tests/out1/nfs.xml > /dev/null
diff -s tests/strength.xml tests/out1/strength.xml > /dev/null
diff -s tests/weakness.xml tests/out1/weakness.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/nfs.xml && rm tests/strength.xml && rm tests/weakness.xml && rm tests/messages.xml
echo "ok"

python ./ElectreNFSOutranking.py -i tests/in3 -o tests
diff -s tests/nfs.xml tests/out1/nfs.xml > /dev/null
diff -s tests/strength.xml tests/out1/strength.xml > /dev/null
diff -s tests/weakness.xml tests/out1/weakness.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/nfs.xml && rm tests/strength.xml && rm tests/weakness.xml && rm tests/messages.xml
echo "ok"

echo "testing ElectreIIPreorder..."
cd ../ElectreIIPreorder

python ./ElectreIIPreorder.py -i tests/in1 -o tests
diff -s tests/ranking.xml tests/out1/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out1/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in2 -o tests
diff -s tests/ranking.xml tests/out2/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out2/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in3 -o tests
diff -s tests/ranking.xml tests/out3/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out3/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in4 -o tests
diff -s tests/ranking.xml tests/out4/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out4/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in5 -o tests
diff -s tests/ranking.xml tests/out5/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out5/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in6 -o tests
diff -s tests/ranking.xml tests/out6/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out6/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in7 -o tests
diff -s tests/ranking.xml tests/out7/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out7/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in8 -o tests
diff -s tests/ranking.xml tests/out8/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out8/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in9 -o tests
diff -s tests/ranking.xml tests/out9/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out9/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"

python ./ElectreIIPreorder.py -i tests/in10 -o tests
diff -s tests/ranking.xml tests/out10/ranking.xml > /dev/null
diff -s tests/messages.xml tests/out10/messages.xml > /dev/null
rm tests/ranking.xml && rm tests/messages.xml
echo "ok"