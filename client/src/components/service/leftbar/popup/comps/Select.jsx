import styles from "./Select.module.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faGlobe} from "@fortawesome/free-solid-svg-icons";

export default function Select({title,icon}){

    return <div className={styles.wrapper} >
        <label className={styles.wrapper__label} > <FontAwesomeIcon icon={icon}/> <span>{title}</span></label>
        <select className={`${styles.wrapper__input} ${styles.wrapper__input_select}`} >
            <option value="ENG">English</option>
            <option value="SK">Slovakia</option>
            <option value="UA">Ukraine</option>
        </select>
    </div>




}