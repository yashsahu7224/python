document.addEventListener('DOMContentLoaded',()=>{
    document.querySelector('#aboutus-container').style.display='none';
    document.querySelector('#waiting').style.display='none';
    document.querySelector('#output').style.display='none';
    document.querySelector('#home').onclick = () => {
        document.querySelector('#aboutus-container').style.display='none';
        document.querySelector('#home-container').style.display='block';
    }
    document.querySelector('#aboutus').onclick = () => {
        document.querySelector('#home-container').style.display='none';
        document.querySelector('#aboutus-container').style.display='block';
    }
    let batting_team=document.querySelector('#id_batting_team');
    let bowling_team=document.querySelector('#id_bowling_team');
    document.querySelector('#id_batting_team').onchange = () => {
        if(batting_team.selectedIndex == bowling_team.selectedIndex)
        {
            alert("Batting and Bowling teams can't be same");
            document.querySelector('#id_batting_team').selectedIndex=0;
        }
    };
    document.querySelector('#id_bowling_team').onchange = () => {
        if(batting_team.selectedIndex == bowling_team.selectedIndex)
        {
            alert("Batting and Bowling teams can't be same");
            document.querySelector('#id_bowling_team').selectedIndex=0;
        }
    };
})
