import React, { useEffect, useState } from 'react'
import api from './api'

function Tag({ children, color = '#7c3aed' }){
  return <span style={{background: 'rgba(255,255,255,0.04)', padding:'6px 10px', borderRadius:10, fontWeight:700, color:'#fff', fontSize:12}}>{children}</span>
}

function ProjectCard({ p, onEdit, onDelete }){
  return (
    <div className="card project-card">
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
        <div>
          <div style={{fontWeight:800,fontSize:16}}>{p.title}</div>
          <div className="muted" style={{marginTop:6}}>{p.description}</div>
        </div>
        <div style={{display:'flex',flexDirection:'column',alignItems:'flex-end',gap:8}}>
          <div className="small muted">{new Date(p.created_at).toLocaleString()}</div>
          <div style={{display:'flex',gap:8,alignItems:'center'}}>
            <Tag>{p.status}</Tag>
            <Tag>{'★'.repeat(Math.max(1, Math.min(5, p.priority || 2)))}</Tag>
          </div>
        </div>
      </div>
      <div style={{marginTop:10, display:'flex', gap:8, justifyContent:'flex-end'}}>
        <button className="btn small" onClick={()=>onEdit(p)}>Edit</button>
        <button className="btn small danger" onClick={()=>onDelete(p)}>Delete</button>
      </div>
    </div>
  )
}

function ProjectForm({ onSave, onCancel, initial }){
  const [title, setTitle] = useState(initial?.title || '')
  const [description, setDescription] = useState(initial?.description || '')
  const [status, setStatus] = useState(initial?.status || 'idea')
  const [priority, setPriority] = useState(initial?.priority || 2)

  const submit = (e)=>{
    e.preventDefault()
    if(!title.trim()) return alert('Title is required')
    onSave({ ...initial, title, description, status, priority })
  }

  return (
    <form onSubmit={submit} className="card form-card">
      <div style={{display:'flex',gap:12,flexDirection:'column'}}>
        <input className="input" placeholder="Project title" value={title} onChange={e=>setTitle(e.target.value)} />
        <textarea className="input" rows={4} placeholder="Short description" value={description} onChange={e=>setDescription(e.target.value)} />
        <div style={{display:'flex',gap:8}}>
          <select className="input" value={status} onChange={e=>setStatus(e.target.value)}>
            <option value="idea">idea</option>
            <option value="active">active</option>
            <option value="completed">completed</option>
            <option value="archived">archived</option>
          </select>
          <input className="input" type="number" min={1} max={5} value={priority} onChange={e=>setPriority(Number(e.target.value))} style={{width:96}} />
        </div>
        <div style={{display:'flex',gap:8,justifyContent:'flex-end'}}>
          <button type="button" className="btn" onClick={onCancel}>Cancel</button>
          <button className="btn btn-start" type="submit">Save</button>
        </div>
      </div>
    </form>
  )
}

export default function App(){
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)

  const load = async ()=>{
    setLoading(true)
    try{
      const res = await api.get('/projects')
      setProjects(res.data)
    }catch(e){ console.error(e); alert('Failed to load projects') }
    setLoading(false)
  }

  useEffect(()=>{ load() }, [])

  async function handleSave(data){
    try{
      if(data.id){
        const res = await api.put(`/projects/${data.id}`, data)
        setProjects(p => p.map(x => x.id === res.data.id ? res.data : x))
        setEditing(null)
      }else{
        const res = await api.post('/projects', data)
        setProjects(p => [res.data, ...p])
      }
      setShowForm(false)
    }catch(e){ console.error(e); alert('Save failed') }
  }

  async function handleDelete(p){
    if(!confirm('Delete this project?')) return
    try{
      await api.delete(`/projects/${p.id}`)
      setProjects(ps => ps.filter(x => x.id !== p.id))
    }catch(e){ console.error(e); alert('Delete failed') }
  }

  return (
    <div className="app-wrap">
      <header className="app-header">
        <div className="logo">PP</div>
        <div>
          <div className="app-title">ProjectPulse</div>
          <div className="muted">Focused project management — lightweight, reliable tracking</div>
        </div>
        <div style={{marginLeft:'auto'}}>
          <button className="btn btn-start" onClick={()=>{ setShowForm(true); setEditing(null) }}>New Project</button>
        </div>
      </header>

      <main style={{display:'grid',gridTemplateColumns:'1fr 420px',gap:20, marginTop:24}}>
        <section>
          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
            <h2 style={{margin:0}}>Projects</h2>
            <div className="muted">{loading ? 'Loading...' : projects.length + ' items'}</div>
          </div>
          <div style={{marginTop:12,display:'grid',gap:12}}>
            {projects.map(p => <ProjectCard key={p.id} p={p} onEdit={(proj)=>{ setEditing(proj); setShowForm(true) }} onDelete={handleDelete} />)}
            {!projects.length && <div className="card muted">No projects yet — create a project to get started.</div>}
          </div>
        </section>

        <aside>
          <div className="card smallpanel">
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
              <div style={{fontWeight:800}}>Quick Actions</div>
              <div className="muted">Presets</div>
            </div>
            <div style={{display:'flex',gap:8,marginTop:12}}>
              <button className="add-btn" onClick={()=>{ setShowForm(true); setEditing({ title:'Sprint', description:'Two-week sprint', status:'active', priority:3 }) }}>Add Sprint</button>
              <button className="add-btn" onClick={()=>{ setShowForm(true); setEditing({ title:'Research', description:'Research task', status:'idea', priority:2 }) }}>Add Research</button>
            </div>
          </div>

          <div style={{height:12}} />

          {showForm && <ProjectForm initial={editing} onSave={handleSave} onCancel={()=>{ setShowForm(false); setEditing(null) }} />}

          <div style={{height:12}} />

        </aside>
      </main>

    </div>
  )
}
