import styles from "./Icon.module.css";
import logo from "../../assets/logo.svg";

export default function Icon(){
    return <div className={styles.icon}>
        <img src={logo} alt="logo"/>
        <p>WebPulsGPT</p>
    </div>
}