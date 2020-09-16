import re
from uuid import uuid4

standardsInput = 'uploads/'
standardsOutput = 'output/mapping/'
# change it as per location of google's news model in your local machine.
modelpath = 'uploads/GoogleNews-vectors-negative300.bin'
s: str = re.split('[-]', str(uuid4()))[-1]

gtfs = 'gtfs.xsd'
netex = 'netex.xsd'
source_rw = 's_SumArray3' + s + '.csv'
target_rw = 't_SumArray3' + s + '.csv'
ontoname = 'it.owl'

write_pathVecRaw = 'SumVecRaw' + s + '.csv'
write_pathVecThr = 'SumVecThr' + s + '.csv'
write_pathVecOrgRaw = 'SumVecOrgRaw' + s + '.csv'
write_pathVecOrgThr = 'SumVecOrgThr' + s + '.csv'

readpathCompound = 'SumVecOrgThr' + s + '.csv'
writepathCompound = 'Sumst_MatchCount' + s + '.csv'
