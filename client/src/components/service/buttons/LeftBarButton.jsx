import styles from './LeftBarButton.module.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export default function LeftBarButton({icon, type,onBarSelect}){


    return <div onClick={()=>onBarSelect(type)} className={styles.leftbar_button}>
        <FontAwesomeIcon icon={icon}/>
    </div>
}