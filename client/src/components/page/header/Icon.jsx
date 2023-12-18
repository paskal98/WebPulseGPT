import styles from "./Icon.module.css";
import logo from "../../../assets/logo.svg";
import {pages} from "../data/pages.js";

export default function Icon({onClickIcon}){
    return <div onClick={()=>onClickIcon(pages[0])} className={styles.icon}>
        <img src={logo} alt="logo"/>
        <p>WebPulsGPT</p>
    </div>
}