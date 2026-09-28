import type {Question} from '../domain/types';
export default function QuestionDiagram({question}:{question:Question}){
 if(!question.diagram)return null;
 return <img className="question-diagram" src={`data:image/svg+xml;charset=utf-8,${encodeURIComponent(question.diagram.svg)}`} alt={question.diagram.alt}/>;
}
export function bankLabel(questions:Question[]){
 if(questions.some(q=>q.dummy))return 'Development preview · Dummy questions and answer keys are not fully checked';
 return questions.every(q=>q.reviewStatus==='sample_reviewed')?'Gables-calibrated practice · Human sample reviewed':'Earlier practice bank · Awaiting human review';
}
