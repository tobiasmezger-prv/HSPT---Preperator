import 'fake-indexeddb/auto';
import {it,expect} from 'vitest';
import {loadSessions,saveSession} from '../src/domain/storage';
import {createSession} from '../src/domain/session';
import {questions} from '../src/data/questions';
it('round-trips a reproducible session for refresh and resume',async()=>{const s=createSession(questions.slice(0,10),'timed','mixed',12345);s.responses['dev-01']={answer:'D',flagged:true,approximateActiveMs:1200};await saveSession(s);const restored=(await loadSessions()).find(x=>x.id===s.id);expect(restored).toEqual(s);s.responses['dev-01'].answer=null;await saveSession(s);expect((await loadSessions()).filter(x=>x.id===s.id)).toHaveLength(1);expect((await loadSessions()).find(x=>x.id===s.id)?.responses['dev-01'].answer).toBeNull();});
