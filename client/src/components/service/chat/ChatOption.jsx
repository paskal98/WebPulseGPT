import styles from './ChatOption.module.css';
import {chatOptions} from "../data/chatOptions.js";

export default function ChatOption({onOptionSelect}){

    function ChatOptionItem(key, title){
        return <div key={key} onClick={()=>onOptionSelect(title)} className={styles.chatoption__item}>{title}</div>
    }

    return <div className={styles.chatoption}>
        {chatOptions.map((item, idx) => ChatOptionItem(idx,item))}
    </div>

}