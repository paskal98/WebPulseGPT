import styles from './HistoryLabel.module.css';

export default function HistoryLabel({idConversation,title, onChatSelected}){


    return <div onClick={()=>onChatSelected(idConversation)} className={styles.convlabel}>{title}</div>

}