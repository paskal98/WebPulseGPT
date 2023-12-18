import styles from './Code.module.css';
import Item from "./Item.jsx";

export default function Code({conversation}){

    return <div className={styles.code}>

        { conversation.files.length>0 && conversation.files.map((item,idx)=> <Item key={idx} title={item.title} description={item.description} version={item.version}/> )}
        { conversation.files.length===0 && <div className={styles.code__warning} >No project files yet</div>}

    </div>

}