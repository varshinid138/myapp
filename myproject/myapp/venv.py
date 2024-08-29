import gym
from gym import spaces
import numpy as np

class ModulePlanningenv(gym.Env):
    def __init__(self, batches_data):
        super(ModulePlanningenv, self).__init__()
        self.batches_data=batches_data
        self.num_batches=len(self.batches_data)
        self.action_space=spaces.MultiDiscrete([10]*self.num_batches)
        self.observation_space=spaces.MultiBinary((self.num_batches,10))
        self.current_state=self.get_initial_state()


    def get_initial_state(self):
        initial_state=[]
        for i in range(self.num_batches):
            initial_state.append(np.zeros(10))
            initial_state[i][self.batches_data[i]]=1
        return initial_state

    def step(self,action):
        self.action=action
        self.reward=self.get_reward()
        for _ in range(self.num_batches):
            self.current_state[_][action[_]]=1
        return self.current_state,self.reward,True,{}
    
    
    def get_reward(self):
        self.initial_state=self.get_initial_state()
        action=self.action
        reward=0
        assignment,a_c=self.check_module_assignement()
        a=np.where(np.array(action)<=5)
        b=np.where(np.array(action)>5)
        c_flow,cf_c=self.check_flow(a)
        d_flow,df_c=self.dynamic_flow(b)
        if assignment&c_flow&d_flow:
            d=self.check_merge()
            if len(d)>0:
                merge=np.array(list(d.values())).sum()
            else:
                merge=0
        else:
            merge=0
        ca=self.num_batches-a_c
        cf=len(list(a[0]))
        df=self.num_batches-cf
        ccf=cf-cf_c
        cdf=df-df_c
        ca_r=1
        wa_r=-12
        ccf_r=1
        wcf_r=-4
        cdf_r=2
        wdf_r=-4
        m_r=10
        uni=set(self.action)
        reward= ((a_c*wa_r)+(cf_c*wcf_r)+(df_c*wdf_r)+(ca*ca_r)+(ccf*ccf_r)+(cdf*cdf_r)+(merge*m_r))*(self.num_batches/len(uni))
        return reward
    def check_module_assignement(self):
        assignment=True
        count=0
        for _ in range(self.num_batches):
            if self.initial_state[_][self.action[_]]==1:
                count=count+1
        if count!=0:
            assignment=False
        return assignment,count

    def check_flow(self,a):
        flow = True
        count=0
        l=list(a[0])
        for _ in l:
            if self.initial_state[_].sum() != self.action[_]:
                flow = False
                count=count+1
        return flow,count

    def dynamic_flow(self,b):
        count=0
        flow=True
        l=list(b[0])
        for _ in l:
            if self.initial_state[_].sum()<=5:
                count=count + 1
                flow=False
        return flow,count

    def check_merge(self):
        d={}
        action=list(self.action)
        for i in action:
            if action.count(i)>1:
                d.update({i:action.count(i)}) 
        return d

    def reset(self):
        self.current_state=self.get_initial_state()
        return self.current_state
