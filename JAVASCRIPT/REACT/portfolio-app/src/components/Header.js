import React, { useEffect, useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEnvelope } from "@fortawesome/free-solid-svg-icons";
import {
  faGithub,
  faLinkedin,
  faMedium,
  faStackOverflow,
} from "@fortawesome/free-brands-svg-icons";
import { Box, HStack } from "@chakra-ui/react";

const socials = [
  {
    icon: faEnvelope,
    url: "mailto: hello@example.com",
  },
  {
    icon: faGithub,
    url: "https://github.com",
  },
  {
    icon: faLinkedin,
    url: "https://www.linkedin.com",
  },
  {
    icon: faMedium,
    url: "https://medium.com",
  },
  {
    icon: faStackOverflow,
    url: "https://stackoverflow.com",
  },
];

const Header = () => {
  //const [isVisible, setIsVisible] = useState(true); // State to track visibility of header
  const headerRef = useRef(null); // Ref to store the header element
  const handleClick = (anchor) => (e) => {
    e.preventDefault()
    const id = `${anchor}-section`;
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  useEffect(()=>{
    let lastScrollTop = 0;

    const HandleScroll = ()=>{
        let scrollTop = window.scrollY || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {
            // Scrolling down
            console.log("Scrolling down");
            //setIsVisible(false)//(if you are using usestate)
            //headerRef.current.style.top = "-200px"; // Hide the header(if you are using useref)
            headerRef.current.style.transform = "translateY(-200px)";
        } else {
            // Scrolling up
            console.log("Scrolling up");
            //setIsVisible(true)//(if you are using usestate)
            //headerRef.current.style.top = "0"; // Show the header(if you are using useref)
            headerRef.current.style.transform = "translateY(0)";
        } 
        lastScrollTop = scrollTop;
      };

      window.addEventListener("scroll", HandleScroll);

      return () => {
        window.removeEventListener("scroll", HandleScroll);
  };
  })

  return (
    <Box
    ref={headerRef}
      position="fixed"
      top={0} // Hide the header when not visible
      left={0}
      right={0}
      translateY={0}
      transitionProperty="transform"
      transitionDuration=".5s"
      transitionTimingFunction="ease-in-out"
      backgroundColor="#18181b"
      zIndex={1000} 
    >
      <Box color="white" maxWidth="1280px" margin="0 auto">
        <HStack
          px={16}
          py={4}
          justifyContent="space-between"
          alignItems="center"
        >
          <nav>
            <a href={socials[0].url}><FontAwesomeIcon icon={socials[0].icon} size="2x" /></a>
            <a href={socials[1].url} style={{marginLeft: '15px'}}><FontAwesomeIcon icon={socials[1].icon} size="2x" /></a>
            <a href={socials[2].url} style={{marginLeft: '15px'}}><FontAwesomeIcon icon={socials[2].icon} size="2x" /></a>
            <a href={socials[3].url} style={{marginLeft: '15px'}}><FontAwesomeIcon icon={socials[3].icon} size="2x" /></a>
            <a href={socials[4].url} style={{marginLeft: '15px'}}><FontAwesomeIcon icon={socials[4].icon} size="2x" /></a>
          </nav>
          <nav>
            <HStack spacing={8}>
            <a href="/#projects-section"  onClick={handleClick('projects')}>Projects</a>
            <a href="/#contactme-section" onClick={handleClick('contactme')}>Contact Me</a>
            </HStack>
          </nav>
        </HStack>
      </Box>
    </Box>
  );
};
export default Header;
