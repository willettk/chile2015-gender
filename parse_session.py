from __future__ import division
from matplotlib import pyplot as plt
import numpy as np

plt.ion()
import pandas as pd

gencolors =('orange','purple')

q = pd.read_csv('question_data.csv')

fig = plt.figure(1,(16,12))
ax1 = fig.add_subplot(341)

q['speaker'].value_counts().plot(kind='bar',ax=ax1,color=gencolors)
ax1.set_ylabel('Count')
ax1.set_title("Gender of speakers")

ax2 = fig.add_subplot(345)

qa=list(q['questions'])
pd.value_counts(list(''.join(qa))).plot(kind='bar',ax=ax2,color=gencolors)
ax2.set_ylabel('Count')
ax2.set_title("Gender of question askers")

c = pd.read_csv('chair_data.csv')

ax3 = fig.add_subplot(349)
c['gender'].value_counts().plot(kind='bar',ax=ax3,color=gencolors)
ax3.set_ylabel('Count')
ax3.set_title("Gender of session chairs")

# Gender of attendees

countrydata = pd.read_csv('map/countries.csv')
names = countrydata['name']
firstnames = [x.split(' ')[0] for x in names]

from sexmachine import detector as gender
d = gender.Detector(case_sensitive=False)
from collections import Counter
genders = [d.get_gender(fn) for fn in firstnames]
cg = Counter(genders)
attendees = list('M'*(cg['male'] + cg['mostly_male'])+'F'*(cg['female'] + cg['mostly_female']))

ax12 = fig.add_subplot(3,4,10)
pd.value_counts(attendees).plot(kind='bar',ax=ax12,color=gencolors)
ax12.set_ylabel('Count')
ax12.set_title("Gender of attendees")

ax4 = fig.add_subplot(342)
qpt = [len(x) for x in q['questions']]
ax4.hist(qpt,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color='k')
ax4.set_xlabel('Questions per talk')
ax4.set_ylim(0,10)

ax5 = fig.add_subplot(346)
mq = [len(x[1]['questions']) for x in q.iterrows() if x[1]['speaker'] == 'M']
fq = [len(x[1]['questions']) for x in q.iterrows() if x[1]['speaker'] == 'F']
ax5.hist(mq,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color='orange',label='Male speaker')
ax5.hist(fq,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color='purple',label='Female speaker')
ax5.set_xlabel('Questions per talk')
ax5.set_ylim(0,10)
ax5.legend(loc='upper right')


# Who asks questions first?
ax6 = fig.add_subplot(3,4,11)
first = [x[1]['questions'][0] for x in q.iterrows()]
pd.value_counts(first).plot(kind='bar',ax=ax6,color=gencolors)
ax6.set_title("Gender of 1st question-askers")
ax6.set_ylim(0,10)

# Does gender of the first speaker affect the subsequent questions?

ax7 = fig.add_subplot(3,4,12)
malefirst_percentagefemaleafter = [x[1]['questions'][1:].count('F')/len(x[1]['questions'][1:]) for x in q.iterrows() if (x[1]['questions'][0] == 'M' and len(x[1]['questions'][1:]) > 0)]
femalefirst_percentagefemaleafter = [x[1]['questions'][1:].count('F')/len(x[1]['questions'][1:]) for x in q.iterrows() if (x[1]['questions'][0] == 'F' and len(x[1]['questions'][1:]) > 0)]
ax7.hist(malefirst_percentagefemaleafter,bins=np.arange(6)/5.,histtype='step',color='orange',range=(0,1),weights=len(malefirst_percentagefemaleafter)*[1./len(malefirst_percentagefemaleafter)],lw=3,label='Male 1st Q')
ax7.hist(femalefirst_percentagefemaleafter,bins=np.arange(6)/5.,histtype='step',color='purple',range=(0,1),weights=len(femalefirst_percentagefemaleafter)*[1./len(femalefirst_percentagefemaleafter)],lw=3,label='Female 1st Q')
ax7.set_ylim(0,1.0)
ax7.set_xlabel('Fraction of subsequent questions asked by females')
ax7.set_ylabel('Fraction of all talks')
ax7.legend(loc='upper right')

# When M/F asks first question, who asks following questions?

ax8 = fig.add_subplot(344)
malefirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'M']
malefirst_femaleafter = ['F'*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'M']
pd.value_counts(list(''.join(malefirst_maleafter+malefirst_femaleafter)),normalize=True).plot(kind='bar',ax=ax8,color=gencolors)
ax8.set_ylabel('Fraction of remaining questions')
ax8.set_title('Male asks 1st Q')
ax8.set_ylim(0,1)

ax9 = fig.add_subplot(348)
femalefirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'F']
femalefirst_femaleafter = ["F"*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'F']
pd.value_counts(list(''.join(femalefirst_maleafter+femalefirst_femaleafter)),normalize=True).plot(kind='bar',ax=ax9,color=gencolors)
ax9.set_ylabel('Fraction of remaining questions')
ax9.set_title('Female asks 1st Q')
ax9.set_ylim(0,1)

# When M/F is speaker, who asks questions?

ax10 = fig.add_subplot(343)
malefirst_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'M']
malefirst_femaleafter = ['F'*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'M']
pd.value_counts(list(''.join(malefirst_maleafter+malefirst_femaleafter)),normalize=True).plot(kind='bar',ax=ax10,color=gencolors)
ax10.set_ylabel('Fraction of questions')
ax10.set_title('Male speaker')
ax10.set_ylim(0,1)

ax11 = fig.add_subplot(347)
femalefirst_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'F']
femalefirst_femaleafter = ["F"*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'F']
pd.value_counts(list(''.join(femalefirst_maleafter+femalefirst_femaleafter)),normalize=True).plot(kind='bar',ax=ax11,color=gencolors)
ax11.set_ylabel('Fraction of questions')
ax11.set_title('Female speaker')
ax11.set_ylim(0,1)

fig.tight_layout()

plt.show()
