import styles from "./Input.module.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export default function Input({title,icon}){

    return <div className={styles.wrapper} >
        <label className={styles.wrapper__label} > <FontAwesomeIcon icon={icon}/> <span>{title}</span></label>
        <input className={styles.wrapper__input} />
    </div>

}