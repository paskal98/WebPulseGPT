import styles from './SignInUp.module.css';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faLowVision} from "@fortawesome/free-solid-svg-icons";
import Button from "../../buttons/Button.jsx";
import ButtonSignWith from "../../buttons/ButtonSignWith.jsx";
import {faDiscord, faGoogle} from "@fortawesome/free-brands-svg-icons";

export default function SignInUp(){
    return <div className={styles.content}>
        <div className={styles.page}>
            <div className={styles.page__signinup}>

                <div className={styles.page__signinup__text}>
                    <div className={styles.page__signinup__text__welcome}>Welcome!</div>
                    <div className={styles.page__signinup__text__undertext}>Please, Enter your details</div>
                </div>


                <div className={styles.page__signinup__field}>
                        <label className={styles.page__signinup__field__label}>Email</label>
                        <input className={styles.page__signinup__field__input} type="text" required/>
                    </div>

                <div className={styles.page__signinup__field}>
                        <label className={styles.page__signinup__field__label}>Password</label>
                        <input className={styles.page__signinup__field__input} type="password" required/>

                        <div className={styles.page__signinup__field__element}>
                            <FontAwesomeIcon icon={faLowVision}/>
                        </div>

                        <div className={styles.page__signinup__field__password_opt}>
                            <div className={styles.page__signinup__field__password_opt__remeber}>
                                <div className={styles.page__signinup__field__password_opt__remeber__button}></div>
                                <div className={styles.page__signinup__field__password_opt__remeber__text}>Remember me</div>
                            </div>
                            <div className={styles.page__signinup__field__password_opt__forget}>Forget Password?</div>

                        </div>

                    </div>

                <div className={styles.page__signinup__button}>
                    <Button title={'Log In'} spec_style={'form_log_in'}/>
                </div>

                <div className={styles.page__signinup__decoration}>
                    <span className={styles.page__signinup__decoration__line}> </span>
                    <div className={styles.page__signinup__decoration__text}>or</div>
                    <span className={styles.page__signinup__decoration__line}> </span>
                </div>

                <ButtonSignWith title={"Google"} faIcon={faGoogle}/>
                <ButtonSignWith title={"Discord"} faIcon={faDiscord}/>

                <div className={styles.page__signinup__additional}>
                    Don’t have account yet? <span className={styles.page__signinup__additional__marked}> Sign up</span >
                </div>

            </div>

            <div className={styles.page__slider}>
                <div className={styles.page__slider__item}>
                    <div className={styles.page__slider__item__title}>Tip #1</div>
                    <div className={styles.page__slider__item__descr}>The detailed description increase accuracy of your answer</div>
                </div>

                <div className={styles.page__slider__pagination}>
                    <div className={`${styles.page__slider__pagination__item} ${styles.page__slider__pagination__item__selected} `}></div>
                    <div className={styles.page__slider__pagination__item}></div>
                    <div className={styles.page__slider__pagination__item}></div>
                    <div className={styles.page__slider__pagination__item}></div>
                    <div className={styles.page__slider__pagination__item}></div>
                </div>
            </div>


        </div>
    </div>
}