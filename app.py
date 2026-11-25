import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import streamlit.components.v1 as components
import json

GARDEN = '<html><style>body{margin:0;background:#102a2a;color:#fff;font-family:system-ui}svg{width:100%;height:490px;display:block}.wing{transform-box:fill-box;transform-origin:center;animation:flap .22s infinite alternate}.glow{animation:pulse 1.5s infinite alternate}.star{animation:pulse 2s infinite alternate}@keyframes flap{to{transform:scaleX(.45)}}@keyframes pulse{to{opacity:.35}}.petal{animation:float 2s infinite alternate}@keyframes float{to{transform:translateY(-5px)}} </style><svg viewBox="0 0 650 490" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#101c38"/><stop offset="1" stop-color="#28564b"/></linearGradient><radialGradient id="light"><stop stop-color="#fff8a0" stop-opacity=".8"/><stop offset="1" stop-color="#fff8a0" stop-opacity="0"/></radialGradient><radialGradient id="zone"><stop stop-color="#c4e98b" stop-opacity=".45"/><stop offset="1" stop-color="#c4e98b" stop-opacity="0"/></radialGradient></defs><rect width="650" height="490" rx="22" fill="url(#sky)"/><g id="stars"/><circle cx="570" cy="52" r="27" fill="#fff2c6"/><circle cx="582" cy="43" r="25" fill="#14233a"/><g id="zones"/><path d="M0 447 Q80 409 160 447 T320 447 T480 447 T650 447 V490 H0Z" fill="#183e35"/><g id="flowers"/><g id="trails"/><g id="bugs"/><g id="best"/><text x="20" y="27" fill="#eaf6c2" font-size="13">✧ THE LITTLE GLOW GARDEN ✧</text><text id="win" x="325" y="477" text-anchor="middle" fill="#fff1ae" font-size="15"/></svg><script>const d=__DATA__,ns=\'http://www.w3.org/2000/svg\';const xy=p=>[35+p[0]*58,425-p[1]*37];function add(id,tag,a){let e=document.createElementNS(ns,tag);Object.entries(a).forEach(([k,v])=>e.setAttribute(k,v));document.getElementById(id).appendChild(e);return e}for(let i=0;i<45;i++)add(\'stars\',\'circle\',{cx:(i*137+29)%640,cy:(i*79+12)%420,r:1+i%3*.4,fill:\'#fff4c9\',class:\'star\',style:`animation-delay:${i%7*.23}s`});for(let i=0;i<16;i++){let x=12+i*42,y=450+(i%3)*10;add(\'flowers\',\'path\',{d:`M${x} 490 Q${x-8} ${y+15} ${x} ${y}`,stroke:\'#79a982\',fill:\'none\',\'stroke-width\':3});let t=add(\'flowers\',\'text\',{x:x-10,y:y+4,\'font-size\':19,class:\'petal\'});t.textContent=[\'🌸\',\'🍄\',\'🌼\',\'🌿\'][i%4]}for(const p of (d.stall?[[7.5,7],[2.5,3]]:[[7.5,7]])){let [x,y]=xy(p);add(\'zones\',\'circle\',{cx:x,cy:y,r:85,fill:\'url(#zone)\'});let t=add(\'zones\',\'text\',{x,y:y-42,\'text-anchor\':\'middle\',fill:\'#e9f7bf\',\'font-size\':12});t.textContent=d.stall?\'🍓 Demand hotspot\':\'✧ Bright region\'}let [bx,by]=xy(d.best);add(\'best\',\'circle\',{cx:bx,cy:by,r:21,fill:\'none\',stroke:\'#fff7cc\',\'stroke-dasharray\':\'4 4\'});d.points.forEach((p,i)=>{let [x,y]=xy(p),[ox,oy]=xy(d.old[i]),f=d.fitness[i];add(\'trails\',\'line\',{x1:ox,y1:oy,x2:x,y2:y,stroke:\'#e6f8aa\',\'stroke-opacity\':.25,\'stroke-dasharray\':\'3 5\'});let g=add(\'bugs\',\'g\',{transform:`translate(${x} ${y})`});g.innerHTML=`<circle class="glow" r="${16+f*22}" fill="url(#light)" opacity="${.25+.75*f}"/><ellipse class="wing" cx="-9" cy="-5" rx="7" ry="10" fill="#d9f4e6" opacity=".8"/><ellipse class="wing" cx="9" cy="-5" rx="7" ry="10" fill="#d9f4e6" opacity=".8"/><ellipse cy="6" rx="8" ry="10" fill="${f>.5?\'#fff39a\':\'#a7b977\'}"/><circle cy="-4" r="8" fill="#d8e6a0"/><circle cx="-3" cy="-5" r="1.5" fill="#263d38"/><circle cx="3" cy="-5" r="1.5" fill="#263d38"/><path d="M-2 -1 Q0 1 2 -1" stroke="#263d38" fill="none"/><circle cx="-5" cy="-2" r="1.5" fill="#f3a9ae"/><circle cx="5" cy="-2" r="1.5" fill="#f3a9ae"/><path d="M-4 -10 l-3 -5 M4 -10 l3 -5" stroke="#d8e6a0" stroke-width="1.5"/>`;let title=document.createElementNS(ns,\'title\');title.textContent=`Firefly ${i+1} • fitness ${f.toFixed(3)}`;g.appendChild(title);g.animate([{transform:`translate(${ox}px,${oy}px)`},{transform:`translate(${x}px,${y}px)`}],{duration:Math.max(80,d.duration),easing:\'ease-in-out\'});});if(d.celebrate){document.getElementById(\'win\').textContent=\'✦ Wonderful! Near-optimal solution found! ✦\';for(let i=0;i<12;i++){let t=add(\'stars\',\'text\',{x:100+i*40,y:70+i%3*30,fill:\'#ffe9a1\',class:\'petal\'});t.textContent=\'✧\'}} </script></html>'

st.set_page_config(page_title='Firefly Garden',page_icon='✨',layout='wide')
st.markdown('''<style>
.stApp {background: radial-gradient(ellipse at top,#24463c,#101f25 65%); color:#f4f6df;}
[data-testid="stSidebar"] {background:#192f32;}
h1,h2,h3 {color:#e9f5ae!important;} p,label {color:#e1eadb!important;}
[data-testid="stMetric"] {background:#263e3b;border:1px solid #47604b;border-radius:18px;padding:15px;}
.stButton button {border-radius:24px;background:#e5efad;color:#20372d;border:0;font-weight:700;}
.stButton button p {color:#20372d!important;}
</style>''',unsafe_allow_html=True)
st.title('✨ Firefly Garden 2.0')
st.caption('A tiny glowing world of swarm intelligence • Interactive learning lab')
st.markdown('Watch little fireflies search for a better solution, one glow at a time. 🌿')
with st.sidebar:
    st.header('🌱 Garden settings')
    scenario=st.selectbox('Learning scenario',['Moonlit garden','Strawberry stall location'])
    n=st.slider('Number of fireflies',5,40,15)
    alpha=st.slider('Randomness (α)',0.,1.,0.18,0.01)
    beta=st.slider('Base attractiveness (β₀)',0.,1.,0.8,0.05)
    gamma=st.slider('Light absorption (γ)',0.,5.,1.,0.1)
    speed=st.slider('Animation delay (seconds)',0.1,1.,0.3,0.1)
    limit=st.slider('Maximum iterations',10,200,60)
    st.caption('Try changing γ to see how distance affects attraction.')

def fitness(p):
    p=np.asarray(p)
    if scenario=='Moonlit garden':
        return np.exp(-np.sum((p-[7.5,7.0])**2,axis=-1)/8)
    return np.maximum(np.exp(-np.sum((p-[7.5,7.0])**2,axis=-1)/5),0.72*np.exp(-np.sum((p-[2.5,3.0])**2,axis=-1)/4))

def reset():
    p=np.random.default_rng().uniform(0,10,(n,2)); f=fitness(p); k=np.argmax(f)
    st.session_state.update(p=p,iteration=0,history=[float(f[k])],best=p[k].copy(),running=False,config=(n,scenario),previous=p.copy())
if st.session_state.get('config')!=(n,scenario): reset()

def step():
    old=st.session_state.p.copy(); p=old.copy(); f=fitness(old); rng=np.random.default_rng()
    for i in range(n):
        for j in range(n):
            if f[j]>f[i]:
                delta=old[j]-p[i]; r2=np.sum((delta/10)**2)
                p[i]+=beta*np.exp(-gamma*r2)*delta
        p[i]+=alpha*2*(rng.random(2)-0.5)
    p=np.clip(p,0,10); scores=fitness(p); k=np.argmax(scores)
    st.session_state.previous=old; st.session_state.p=p; st.session_state.iteration+=1
    if scores[k]>fitness(st.session_state.best): st.session_state.best=p[k].copy()
    st.session_state.history.append(float(fitness(st.session_state.best)))

c1,c2,c3,c4=st.columns(4)
if c1.button('▶ Start',use_container_width=True): st.session_state.running=True
if c2.button('⏸ Pause',use_container_width=True): st.session_state.running=False
if c3.button('🐝 Next iteration',use_container_width=True,disabled=st.session_state.iteration>=limit):
    st.session_state.running=False; step()
if c4.button('↻ Reset garden',use_container_width=True): reset()
if st.session_state.running and st.session_state.iteration<limit: step()
if st.session_state.iteration>=limit: st.session_state.running=False
p=st.session_state.p; f=fitness(p); best=float(fitness(st.session_state.best))
a,b,c=st.columns(3); a.metric('🌙 Iteration',st.session_state.iteration); b.metric('✨ Best fitness',f'{best:.3f}'); c.metric('🌼 Fireflies',n)
left,right=st.columns([1.65,1])
with left:
    st.subheader('🌿 Explore the garden')
    payload=json.dumps(dict(old=st.session_state.previous.tolist(),points=p.tolist(),fitness=f.tolist(),best=st.session_state.best.tolist(),duration=int(speed*850),stall=scenario=='Strawberry stall location',celebrate=best>=.98))
    components.html(GARDEN.replace('__DATA__',payload),height=510)
    st.caption('✦ Firefly • white ring = best location found so far • brighter background = higher objective value')
with right:
    st.subheader('📈 Glow progress')
    h=go.Figure(go.Scatter(y=st.session_state.history,mode='lines+markers',line=dict(color='#e6f59c',width=3),fill='tozeroy'))
    h.update_layout(height=260,margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor='#192f32',plot_bgcolor='#192f32',font_color='#e5efcf',xaxis_title='Iteration',yaxis_title='Best fitness',yaxis_range=[0,1.05])
    st.plotly_chart(h,use_container_width=True,config={'displayModeBar':False})
    if scenario=='Strawberry stall location':
        st.markdown('### 🍓 Strawberry stall mission')
        st.write('Find a stall location with the highest estimated customer demand. Two promising areas compete for attention.')
        st.metric('Estimated customers/day (toy model)',round(best*100))
    else:
        st.markdown('### 🌙 Garden mission')
        st.write('Find the brightest region of the garden. Each firefly represents a possible position.')
    st.progress(min(1.,best),text='Best fitness relative to known model maximum')
    if best>=.98: st.success('✨ Lovely! A near-optimal location has been found.')
with st.expander('📖 Learning corner — How does it work?',expanded=True):
    st.markdown('**Brightness:** solution quality. **Attraction:** movement towards better candidates. **Distance:** distant candidates exert weaker attraction when γ > 0. **Randomness:** exploration of new positions.')
    st.latex(r'\beta(r)=\beta_0 e^{-\gamma r^2}')
    st.write('This teaching variant uses synchronous brightness comparisons, normalized distance, bounded positions and a random perturbation per firefly per iteration. The best-so-far solution is retained separately.')
    st.markdown('**Try it:** Reset the garden, set α to zero, and compare the results with α = 0.5. Does more exploration always help?')
    st.markdown('**Reading:** [Yang (2010), Firefly Algorithms for Multimodal Optimization](https://arxiv.org/abs/1003.1466) · [Fister et al. (2013), A comprehensive review of firefly algorithms](https://doi.org/10.1016/j.swevo.2013.06.001)')
st.caption('Made for CE learning • Synthetic objective functions, not real customer data • No guarantee of global optimality')
if st.session_state.running:
    time.sleep(speed); st.rerun()
