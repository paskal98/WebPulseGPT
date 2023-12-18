import styles from './Button.module.css'
import {popUps} from "../../../data/popUps.js";

export default function Button({title,type,onBarSelect}){

    let style = `${styles.button} `;
    if (type==='save'){
        style+=`${styles.save}`;
    } else if(type==='exit'){
        style+=`${styles.exit}`;
    }

    return  <button onClick={()=>onBarSelect(popUps[0])} className={style} >{title}</button>

}