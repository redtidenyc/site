BEGIN TRANSACTION;
CREATE TABLE "django_flatpage" (
    "id" integer NOT NULL PRIMARY KEY,
    "url" varchar(100) NOT NULL,
    "title" varchar(200) NOT NULL,
    "content" text NOT NULL,
    "enable_comments" bool NOT NULL,
    "template_name" varchar(70) NOT NULL,
    "registration_required" bool NOT NULL
, "mimetype" varchar(256) NOT NULL default "text/html");
INSERT INTO "django_flatpage" VALUES(1,'/contact/','Contact Redtide','<h1>Contact Us</h1>

<h3>Team Membership Questions</h3>
 <p><a href="mailto:info@redtidenyc.org?subject=Question About Membership">info@redtidenyc.org</a> <br />(enter ''Question About Membership'' in subject line)</p
>
                
            <h3>Registration Questions/Problems</h3>
            <p><a href="mailto:help@redtidenyc.org?subject=Registration Question">help@redtidenyc.org</a> <br />(enter ''Registration Question'' in subject line)</p>
                
            <h3>Membership Cancellations</h3>
            <p><a href="mailto:help@redtidenyc.org?subject=Membership Cancellation Request">help@redtidenyc.org</a> <br />(enter ''Membership Cancellation Request'' in subj
ect line)</p>
                
            <h3>Red Tide Board</h3>
            <p><a href="mailto:rtboard@redtidenyc.org">rtboard@redtidenyc.org</a></p>
                
            <h3>Membership Email-Address Changes</h3>
            <p><a href="mailto:webmaster@redtidenyc.org?subject=Change My Email">webmaster@redtidenyc.org</a> <br />(enter ''Change My Email'' in subject line)</p>
                
            <h3>Webmaster</h3>
            <p><a href="mailto:webmaster@redtidenyc.org">webmaster@redtidenyc.org</a></p>',0,'',0,'text/html');
INSERT INTO "django_flatpage" VALUES(2,'/links/','Links to Swimming Resources','<h1>Links</h1>

            <div class="redline"><h2>Governing Bodies</h2></div>
                
            <h3>Metropolitan LSMC</h3>
            <p>Home page of Metro Area Masters Swim Committee, our local governing body. Contains info and links to all registered Masters clubs in the tri-state area.<br
/>

            <a href="http://www.metroswim.org/">http://www.metroswim.org/</a></p>
                
            <h3>United States Masters Swimming</h3>
            <p>Home page of US Masters Swimming. Contains listing and links of all Masters teams and local swim committees, training, workouts, competitions, places to sw
im, and message board.<br/>
            <a href="http://www.usms.org/">http://www.usms.org/</a></p>
                
            <h3>USA Swimming</h3>
            <p>Official website for USA Swimming.<br/>
            <a href="http://www.usaswimming.org/usasweb/DesktopDefault.aspx">http://www.usaswimming.org/usasweb/DesktopDefault.aspx</a></p>
            <h3>FINA: World Swimming Organization</h3>
            <p>La F&eacute;d&eacute;ration Internationale de Natation Amateur, the international governing body overseeing diving, swimming, water polo, and synchronized 
swimming and containing news, international competitions, and rules.<br/>
            <a href="http://www.fina.org/">http://www.fina.org/</a></p>

            <div class="redline"><h2>Resources</h2></div>
                        
            <h3>Swimming World Magazine</h3>
            <p>The World''s Leading Independent Resource for Swimming<br/>
            <a href="http://www.swimmingworldmagazine.com/Default.asp">http://www.swimmingworldmagazine.com/Default.asp</a></p>
                
            <h3>Time Conversion Utility</h3>
            <p>Convert yards to meters, and vice versa<br/>
            <a href="http://www.swimmingworldmagazine.com/results/conversions.asp">http://www.swimmingworldmagazine.com/results/conversions.asp</a></p>
                
            <h3>Swimmers'' Guide Pool Database</h3>
            <p>To get pool info in the US and around the world<br/>
            <a href="http://www.swimmersguide.com/query/Main1.cfm">http://www.swimmersguide.com/query/Main1.cfm</a></p>
                                
            <h3>Sports Camps International</h3>
            <p>Organizers of our swim camp<br/>
            <a href="http://www.swim-camps.com/">http://www.swim-camps.com/</a></p>
  
            <div class="redline"><h2>Health</h2></div>
                
            <h3>The Physician and Sports Medicine Info Online</h3>
            <p><a href="http://www.physsportsmed.com/">http://www.physsportsmed.com/</a></p>
                                
            <h3>Swimming Biomechanics and Injury Prevention</h3>
            <p><a href="http://www.physsportsmed.com/issues/2003/0103/johnson.htm">http://www.physsportsmed.com/issues/2003/0103/johnson.htm</a></p>
                
            <h3>Shoulder Strengthening Exercises for Swimmers</h3>
            <p><a href="http://www.physsportsmed.com/issues/2003/0103/johnson_pa.htm">http://www.physsportsmed.com/issues/2003/0103/johnson_pa.htm</a></p>
                
            <div class="redline"><h2>New York Swimming/Triathlon</h2></div>
                
            <h3>Metro Tri</h3>
            <p>The NY Metropolitan Region''s Multi-sport Resource<br/>
            <a href="http://www.metrotri.com/">http://www.metrotri.com/</a></p>
                
            <h3>Manhattan Island Foundation</h3>
            <p>Organizes swimming events in the waters around Manhattan<br/>
            <a href="http://swimnyc.org/">http://swimnyc.org/</a></p>
                        
            <div class="redline"><h2>Gear</h2></div>
                
            <h3>Kastaway Swimwear</h3>
<p><a href="http://www.kastawayswimwear.com/">http://www.kastawayswimwear.com/</a></p>      
                
            <h3>Kiefer</h3>
            <p><a href="http://www.kiefer.com">http://www.kiefer.com</a></p>
                
            <h3>Splishwear</h3>
            <p><a href="http://www.splishwear.com">http://www.splishwear.com</a></p>
                
            <h3>EQS Swimwear</h3>
            <p><a href="http://www.eqswimwear.com/">http://www.eqswimwear.com/</a></p>',0,'',0,'text/html');
INSERT INTO "django_flatpage" VALUES(3,'/swimminginfo/','General Swimming Info','<h1>Swimming Information</h1>
            
            <div class="redline" id="eti"><h2>Swimming Etiquette</h2></div>
                
            <h3>On Deck</h3>
            <p>Be there at least 5 minutes before the start of the work out. Get your equipment ready. Take a shower. Don''t get in the pool until a coach is on deck.</p>

            <h3>Team Work</h3>
            <p>While swimming might seem like a very individual activity, it actually requires a lot of collaboration. It is important that you are aware of your surround
ings and work with others in the lane to make your workout run smoothly. During the beginning of the workout, take stock of your place in the lane. Assess your strengths 
and weaknesses. Knowing this will make figuring out who is going to lead the lane an easier task. Maybe you will lead a kick set, but stay in back during the pull sets, o
r vice versa. As you learn about yourself and your lane-mates, be sure to communicate with them, especially when there is a choice to swim a different stroke.</p>

            <h3>Know The Set</h3>
            <p>Workouts can be fast-paced affairs, not leaving much time for long explanations of each set. Be sure to listen carefully to the coach when he or she is giv
ing the set. Everyone should understand the entire set before taking off.</p>

            <h3>Watch The Clock</h3>
            <p>Whether you are leading the lane or bringing up the rear, you should be responsible for keeping track of the number of laps you are swimming and the interv
als you are leaving on. (Check out www.wsumastersswimming.org/workouts/paceclock.html for a great description and explanation of reading a pace clock.) If the set is part
icularly long or complicated, you might want to make it a team effort and assign one person to count and another to watch the intervals. However, every swimmer sho
uld be aware of where you are in the set and when you are coming in. If it is a sprint set, know what times you are "holding" or coming in on each time. If you have diffi
culty seeing or reading the clock, you might want to try getting a wrist watch to synch with the pace clock.</p>

            <h3>Leave Five (Or Ten)</h3>
            <p>It is important to maintain an adequate distance between swimmers in the lane. If you leave less than five seconds behind the person in front of you, you w
ill end up drafting off of them and probably catching up to them. This is frustrating for everyone. If there are only a few people in the lane, you might want to leave te
n seconds to make it easier on everyone.</p>

            <h3>Respect Your Leader</h3>
            <p>The leader of a set is responsible for establishing the pace of the set. A good leader will pace the entire lane and won''t "blow it out" on the first set a
nd then die on the next ones. Remember that during challenging and longer distance sets, the leader of the lane will inevitably be working very hard. Even allowingfive se
conds between swimmers, everyone is usually drafting off the leader. This will slow the leading swimmer down. If everyone is swimming at the same speed, trade off leading
 the sets, rather than trying to pass the leader in the middle of a set.</p>

            <h3>Getting Lapped</h3>
            <p>During longer distance sets, lapping is often inevitable. This is when the leader of the lane catches up to and passes the last person in the lane. With ma
ny people in the lane, you may be at a particular disadvantage at the head or rear of the lane when the first swimmer is leaving 30 or 40 seconds ahead of the last. Every
one should be aware of where the others in the lane are.</p>

            <ul>
                <li>If you approach someone in front of you, tap their feet so they know that you are there. If you are in the middle of the lane, and feel strong and con
fident, you can pass them. Do this quickly and carefully. Make sure you are not going to cause a head-on collision.</li>
                <li>Try to avoid passing someone at the very end of the set, like on the last 25 of a 200. In that case, wait until you come to the wall and ask the perso
n in front of you if you can go ahead of them.</li>
                <li>If you get tapped in the middle of the lane, swim closer to the lane lines to allow the person to pass you. Slow down a little to let them pass,  this
 isn''t a race.</li>
            <li>If you see someone coming up on you as you are turning (actually if you don''t see the person behind you, it probably means they are very close), you might
 want to think about pausing at the end of the next lap. In that case, pull to the right at the wall and allow the next swimmer to do a flip turn and proceed. Give them f
ive seconds before taking off (or three if it''s really crowded). Try to avoid inserting yourself immediately between two swimmers. This will just get everyone bunched up.
</li>
            </ul>

            <p><strong>Don''t take it personally. Everyone has their good days and bad days.</strong></p>

            <h3>Lane Spirit</h3>
            <p>While you may be swimming in a pool with 40+ people, your lane makes up its own little community. A lane that works well together will make the workout fee
l good, even if it is challenging. Motivate your lane mates with a little positive feedback. Even a "let''s go" can cheer you up in the middle of a discouraging set. </p>
<div class="redline" id="lingo"><h2>Swimming Lingo</h2></div>
                
            <p class="intro">Every group establishes their own language and swimming is no exception, here are some terms that you might hear during a workout:</p>
                
            <h3>Warm-up</h3>
            <p>This is an essential part of the workout. A good warm up allows your muscles to loosen and warm up. Swim slowly at an easy pace. Your heart rate should not
 be increased much during the first half of the warm up. A normal warm-up is about 1200 to 1500 yards. Wait until the coach gives the warm up to begin swimming.</p>
                 
            <h3>Pulling</h3>
            <p>An exercise that uses just your arms. This usually involves putting a pull buoy or a kick board between your legs to suspend them.</p>
                
            <h3>Drill</h3>  
            <p>A general term for doing technique specific work during a set. There are many different types of drills and often the coach will explain exactly what he or
 she wants you to do. After swimming for a while, you will develop a repertoire of drills for each stroke that you may be called upon to use when an imprecise "drill a 50
" is offered.</p>
                
            <h3>Descend</h3>
            <p>For example, if you are told to do "4 x 100 descend," you want to come in faster on each successive 100. Take the first one slowly and build your speed on 
each 100. Look at the clock so you can tell how much you are "descending" or taking off each 100.</p>
                
            <h3>Build</h3>
            <p>To "build a 50" means to increase your speed over the course of the 50 yards so that you are sprinting into the finish.</p>
                
            <h3>Breakout</h3>
            <p>The first couple strokes after the push off. In breast-stroke, the break out is a strong kick and a stroke underwater. In the other strokes, it is 3-4 stro
ng kicks under water and your first 2 strokes.</p>
                
            <h3>Pace Work</h3>
            <p>Keeping the same time and speed during a set. This usually implies going at a moderate speed in order to maintain the same time throughout a set.</p>
                
            <h3>Race Pace</h3>
            <p>Some sets are meant to replicate a meet, so you will be asked to go "100 race pace for a 50." This means that you swim as fast as you would in a 100 yd rac
e, but you only swim half that distance.</p>
                
            <h3>Main Set</h3>
            <p>As it sounds, this is the set that you have been warming up for. It is a chance to work hard.</p>
                
            <h3>Recovery</h3>       
            <p>A recovery or "easy" set is often given between sets or after a hard set. This is also called "active rest." Take it slow, use it to recover, and let your 
heart rate return to normal.</p>

            <h3>Cool Down</h3>
            <p>This is the last part of the workout, but it is very important, especially if you have been sprinting or raising your heart rate. The cool down is a recove
ry set that allows the lactic acid built up in your muscles to dissipate. Cooling down properly helps avoid muscle soreness.</p>',0,'flatpages/swimminginfo.html',0,'text/html');
INSERT INTO "django_flatpage" VALUES(4,'/howtojoin/','How To Join Redtide','<h1>Join Red Tide</h1>    
            <div class="redline" id="team"><h2>How to Join</h2></div>
            <p class="intro">There are three distinct steps for swimming with Red Tide Masters.  The first is obtaining a current (must be renewed yearly) membership with
 United States Masters Swimming (USMS).  The second is choosing which fee option works best for you:  monthly unlimited, SwimPass, "Hour of Power" SwimPass, or drop-in.  
The third is registering for your preferred payment option online and following the directions.</p>
            
            <h3>Step 1: USMS Membership is a MANDATORY PRE-REQUISITE</h3>
            <p>Membership with USMS as evidenced by a member card and number for the current year (must be renewed yearly).   This is an off-line operation which much be 
completed in advance of registering for any of the Red Tide payment options.  Click on the link below to download and view the USMS Membership Form, print it out, complet
e the form, and send it to the address specified along with a check for the amount requested to USMS.</p>
            
            <p> <a id="usms_form" href="/static/pdfs/rt_usms06-07_nov.pdf" target="_blank">USMS Membership Form</a></p>

            <h3>Step 2: Fee Options</h3>

            <p>There are several fee options: monthly unlimited, SwimPass, or drop-in.  You can choose which suits your swimming schedule best.  Current prices and direct
ions are listed on the Registration page.</p>
            
            <p><strong>Monthly unlimited</strong> is the most cost effective option if you are swimming two or more times per week on a regular basis.  The cost is $95 pe
r month, for a minimum of two months.</p>

            <p><strong>SwimPass</strong> is a punch card option that is priced at a higher rate per swim than the monthly unlimited, but cheaper than drop-in.  The card c
osts $120 for 10 swims and is valid for three months from the date of purchase.</p>
           
            <p><strong>"Hour of Power" SwimPass</strong> is a punch card that is priced like the  SwimPass.  The card costs $100 for 10 swims and is valid for three month
s from the date of purchase.   However, it is valid for the one hour workouts ONLY.  This card is not good for the 1.5 or 2 hours workouts.</p>
 
            <p><strong>Drop-in</strong> is a per swim fee paid at each workout attended.  The fee is $15, which must be presented along with a current USMS card and/or cu
rrent Red Tide Member card.</p>
        
            <h3>Step 3: REGISTRATION:  Annual Membership & Selection of Fee Option</h3>
            
            <p>All registration is handled online and fees are payable via PayPal.  If you do not currently have a PayPal account,  click on the link below.  It is easy a
nd fast to set up an account.  Click <a href="http://www.paypal.com">here</a> to set up a paypal account.</p>

            <p><strong>You must have your current USMS membership number in order to register.</strong></p>

            <p><strong>Monthly Unlimited:</strong> This lowest rate available per swim is payable automatically via PayPal. There is a minimum commitment of two months in
 order to enjoy this low rate.  The annual member fee will be added to the first monthly payment.  After registering online, monthly unlimited members <span style="text-d
ecoration: underline;">must bring their PayPal receipt and a copy of their current USMS card in order to receive their Red Tide Member card</span>.  This Red Tide Member 
card must be brought to every practice.</p>

            <p><strong>SwimPass and "Hour of Power" SwimPass:</strong> The punch card SwimPasses are purchased online via PayPal.  The annual member fee will be added to 
the cost of the first SwimPass purchased.  <span style="text-decoration: underline;">After purchase, you must bring a copy of the PayPal receipt and a copy of your USMS c
ard to either pool in order to receive your SwimPass and Red Tide Member Card</span>.  After you receive your Red Tide member card, you need only bring your Paypal receip
t for subsequent punchcards.</p>

            <p><strong>Drop in:</strong> Sign up for annual membership online. <span style="text-decoration: underline;">You must bring a copy of your receipt and a copy 
of your USMS card to the pool and receive a Red Tide Member card.</span>   Drop in fee is $15 per swim payable each time at the pool. You will need to present your Red Ti
de member card or USMS card each practice you attend in order to swim.</p>

            <p>The Red Tide annual member fee is a small one time charge of $40 to all members, regardless of fee option.</p>

            <p><strong>Registration:</strong>  <a href="/register/" class="red_link">Click here for Registration</a>.</p>

            <p><strong>Cancellations:</strong> The annual Red Tide membership fee and Swimpass cards are  non-refundable. The monthly unlimited option is cancelable any t
ime after two months.  In order to cancel your monthly subscription, you need to send an email to the registrar. 30 days advance notice to cancel is recommended to allow 
for time to process through PayPal.</p>',0,'flatpages/howtojoin.html',0,'text/html');
INSERT INTO "django_flatpage" VALUES(5,'/tri/','Triathlon Training With Red Tide','<h1>Red Tide Triathletes</h1>
            
            <div class="highlightbox">
                
                <div class="redline" id="lingo">
                <h2>Spring Update: SBR Partnership</h2>
                </div>
                
                <div class="rightchunk">
                    <a href="http://www.sbrshop.com/" target="_blank"><img src="/media/img/sbr_logo.gif" border="0" height="93" width="150"></a><br>
                </div>
                
                <p class="intro"><span style="font-size:10px">Red Tide is proud to announce a new partnership with the SBR Triathlon Club!  The SBR Triathlon Club is a US
AT registered club that welcomes beginner, intermediate & elite triathletes who are looking to have fun, get in shape and meet other athletes in the NY area.  The SBR Tri
 Club has workouts 6 days a week, including the new "Hour of Power" swim workouts with Red Tide.  SBR''s morning and evening workouts incorporate swimming, biking, running and brick workouts led by the SBR Ambassadors, a team of 12 experienced triathletes.</span></p>

                <p><span style="font-size:10px">The SBR Triathlon Club is based out of SBR Multisports, a triathlon shop in NYC, located one block from Central Park. SBR 
Multisports features the latest triathlon equipment including bikes, wetsuits, swim/bike/run apparel, and nutrition products.  Please visit us online at www.sbrshop.com a
nd stay tuned with our new products, bi-weekly newsletters, events and clinics, summer triathlon series, and the SBR Triathlon Club.  For more information please visit <a
 href="http://www.sbrshop.com/" target="_blank">www.sbrshop.com</a> or contact <a href="mailto:Alison@sbrshop.com">Alison@sbrshop.com</a>.</span></p>
            </div>
            
        
        <div class="redline"><h2>Try Red Tide for Tri Training</h2></div>
            
            
            <p class="intro">For many triathletes the swim is the toughest of the three events and training on one''s own can be a real challenge! Most gyms, if they have 
a pool, have a short one, maybe 20 yards (and shallow too). We swim in full, competition-length pools, either 25 yards or 25 meters. During the summer, we coordinate pool
 time with other local master teams and sponsor workouts in an Olympic-distance 50 meter pool. A great experience for open water and tri competitions!</p>
                        
            <p>Some triathletes feel that the swim is the least important of the events, especially as the races get longer (from Olympic to half to full Iron). Nothing c
ould be further from the truth. Red Tide Masters swimming, from novice to experienced triathlete, will help you reach your goals. We focus on:</p>
                        
            <h3>Camaraderie</h3>
            <p>Motivating you to get up and get out is tough. Make friends with others who can ''push'' you.</p>

            <h3>Year Round Training</h3>
            <p>You can''t bike outside during the winter, and at best, you need to run indoors on treadmills. We swim year round in top quality pools at colleges in NYC, r
unning 10 scheduled workouts per week: mornings, evenings, and weekends.</p>
                
            <h3>Structured Workouts:</h3>
            <p>Improve your times and improve the quality of your swim workouts.</p>
                
            <p>Every workout is <em>structured</em>. Many Masters teams are more ''casual'' in their approach. Red Tide has a proud history of carefully structuring every w
orkout to make it matter. Every swim has:</p>
            <ul>
                <li>A warm up (swim, kick, drill)</li>
                <li>Pre-set to increase readiness for the Main Set</li>
                <li>Main-set (the core of any good workout), sometimes focusing on speed, strength or stamina, depending on the time of year. (Yes, we have a full year''s 
plan).</li>
                <li>Finally, the Cool-down</li>
                <li>Occasionally we do dry land work to build additional strength (calisthenics, etc.)</li>
            </ul>
            
            <p>Practicing strokes other than freestyle is indispensable for the triathlete. It balances muscle groups, increases flexibility, and reduces injury. We run r
egular clinics to improve your freestyle as well as the other strokes (back, breast and fly). We''ll help you improve your basics and get you moving!</p>

            <h3>NYC Triathlon Resources:</h3>
            <p><strong>Metro Tri</strong><br/>
            The NY Metropolitan Region''s Multi-sport Resource<br/>
            <a href="http://www.metrotri.com/" target="_blank">www.metrotri.com</a></p>

            <p><strong>Triathlon Association of New York</strong><br/>
            <a href="http://www.tanyc.org/" target="_blank">www.tanyc.org</a></p>',0,'flatpages/tri.html',0,'text/html');
INSERT INTO "django_flatpage" VALUES(6,'/faq/','Registration FAQ','<h1>Registration FAQ</h1>
                <p><strong>Can I cancel my PayPal subscription?</strong></p>
                <p>You may cancel your PayPal subscription whenever you like, but remember that you''ve prepaid one month''s fee.</p>
                <p>For example, if you registered on February 1 and you''d like your subscription to end at the end of April, you must cancel your subscription before PayP
al withdraws the payment for May from your account on April 1. </p>
                <p>You can check when the next payment is going to be charged by logging in to your PayPal account and looking at your subscription details.</p>
                <p><strong>I forgot my PayPal password. What should I do?</strong></p>
                <p>Go to <a href="http://www.PayPal.com" target="_new" class="red_link">PayPal</a> and enter the email account you used to set up the account. (If you can
not remember which one you used, try each one of them systematically.)</p>
                <p>Click on "Forget your password?" link right below password box.</p>
                <p>PayPal will email your password to you. There is also another link in the top right corner entitled "Help with this page" that itemizes common problems
.</p>
                <p><strong>No matter how carefully I type, I get an error message saying my USMS number is invalid. What''s going on?</strong></p>
                <p>Make sure you are looking at your current USMS card. Two of the characters change each year. </p>
                <p>Check the date and time on your computer. If you don''t know how to do that, try another computer.</p>
                <p>If your number does not begin with "06" it means you are not registered with our LMSC. <a href="mailto:help@redtidenyc.org?Subject=Qn: Red Tide Online 
Registration">Contact</a> us to find out what to do.</p>
                <p><strong>Why is the program saying I owe a late fee? The late date hasn''t happened yet.</strong></p>
                <p>Check the date and time on your computer. Reset it if it is wrong. </p>
                <p>If you don''t know how to do that, try another computer.</p>
                <p><strong>Can I use my PayPal account to pay for someone else''s swims?</strong></p>
                <p>Yes! We send the swimmer''s information to our PayPal records so we can tell who gets the swim pass.</p>
                <p><strong>I use Safari and the back and forward buttons don''t work</strong></p>
                <p>They sure don''t. Safari is broken. <a href="http://codinginparadise.org/weblog/2005/09/safari-no-dhtml-history-possible.html">The reason</a> I''d tell A
pple what for</p>
',0,'flatpages/faq.html',0,'text/html');
INSERT INTO "django_flatpage" VALUES(7,'/terms/','Terms','<h1>Red Tide of NYC, Inc. Terms and Agreements</h1>

                <h1>Terms of Membership</h1>

            <p>The following are terms of a legal agreement between you and Red Tide of NYC, Inc. (Red Tide). By submitting your online registration form and becoming a Red Tide member, you acknowledge that you have read, understood, and agree to be bound by these terms and to comply with all applicable laws and regulations and applicable provisions of Red Tide by-laws and USMS rules.</p>

            <p>You agree to provide true, accurate, current and complete information about yourself as prompted by the registration form. If you provide any information t
hat is untrue, inaccurate, not current or incomplete, or if we have reasonable grounds to suspect that such information is untrue, inaccurate, not current or incomplete, 
Red Tide has the right to terminate or suspend your account, and refuse you any and all current or future access to Red Tide services. The Red Tide Board reserves the rig
ht to revise these terms and/or adjust the fee rates at any time and without prior notice.</p>

            <p><strong>Local Masters Swim Committee (LMSC) membership fee</strong></p>

            <p>All Red Tide members must join the Metro LMSC (MLMSC), which is a local chapter of United States Masters Swimming (USMS). This involves a separate fee and 
should not be confused with the Red Tide annual membership fee.</p>

            <p>Payments should be made by mailing a separate check and membership form to the registrar of the MLMSC. We require that you use the Red Tide specific MLMSC 
membership form, which can be downloaded and printed from the Red Tide website. Please refer to the "Fees" page on the website for more details.</p>

            <p>If you are already a Red Tide affiliated MLMSC member then you must renew your LSMC membership in the late Fall of every year.</p>

            <p>If you are currently a member of USMS and are affiliated with another team you must transfer your membership to Red Tide. To do this, please go to the MLMS
C website and follow the relevant instructions. There is a small fee incurred by the MLMSC for transfer of membership.</p>

            <p><strong>Red Tide Fees</strong></p>

            <p>Fees associated with membership to Red Tide are as follows.</p>

            <p>1. Annual Red Tide Membership Fee: $40. The annual fee is assessed upon joining Red Tide and then annually in January thereafter. Upon payment of the fee y
ou will be added to the team roster and e-mail distribution list.</p>

            <p>2. Monthly workout fee: $95. This entitles you to unlimited attendance at any of our regularly scheduled workouts. Payments are debited from your credit ca
rd or checking account via PayPal. For more details, please refer to the Red Tide Fee Payment Policy below.</p>

            <p>3. SwimPass:  This is a punchcard purchased online.  SwimPasses are distributed at the pool upon presentation of your PayPal receipt and a copy of your cur
rent USMS card.  The SwimPass is valid for three months from the date of purchase.</p>

            <p>4. Drop-in fee</p>

            <p>a. $15 per workout for Red Tide members payable at the pool</p>

            <p>b. $5 per workout for out-of-town visitors affiliated with a USMS team payable at the pool.</p>

            <p>Drop in fees are to be paid in cash prior to the start of each workout attended. Drop-in swimmers are asked to please bring a current USMS membership card 
to every attended practice.</p>

            <p><strong>Red Tide Fee Payment Policy</strong></p>

            <p>Red Tide offers credit card or checking account auto payments for monthly fees or SwimPass through PayPal merchant service.  After the initial debit of mem
bership fees from your account, billing will take
place automatically until you request for deactivation in writing (see below cancellation policy). All swimmers should bring their PayPal receipt and USMS card to the fir
st week of practices.</p>

            <p>Monthly membership to Red Tide requires a minimum commitment of two months. </p>
<p>By submitting this form, you authorize Red Tide to charge your credit card or checking account for services and/or products provided by Red Tide. You also 
agree that you require no additional notices prior to action being taken on this authorization. In addition, you agree that if you decide to discontinue the monthly payme
nt method, you will notify Red Tide at least 30 days in advance of terminating membership status.</p>

            <p><strong>Cancellation Policy</strong></p>

            <p>Red Tide does not offer refunds on program fees. You may cancel your monthly unlimited fee option  by submitting a request in writing with 30 days notice. 
You may restart your monthly fee option by going through the registration process again.</p>

            <p><strong>Copyrights</strong></p>

            <p>The Red Tide logo, all designs, text, and graphics on the website, are the property of Red Tide. Any use of the Red Tide logo or materials on the website w
ithout written prior consent is prohibited.</p>

            <p><strong>Red Tide of NYC, Inc. Release from Liability</strong></p>

            <p>I, the submitting participant, intending to be legally bound, hereby certify that I am physically fit and have not been informed otherwise by a physician. 
I acknowledge that I am aware of all the risks inherent in swimming (training, competition and/or recreational), including possible injury, illness, disability or death, 
howsoever caused or arising, and knowingly and willingly agree to assume all of those risks.</p>

            <p>As a condition of participation, I, the undersigned, on my own behalf and on behalf of my heirs, legatees, beneficiaries, executors, administrators, legal 
representatives, successors and assigns, hereby agree that I am voluntarily participating and hereby assume all risk of injury, illness, disability or death, howsoever ca
used or arising, and do hereby indemnify, remise release, discharge and forever hold harmless Red Tide of NYC, Inc. and any pool facility administering organizations and 
their respective affiliates, parents, subsidiaries, directors, officers, partners, members, managers, shareholders, employees, agents, attorneys, representative, successo
rs and assigns (collectively, the "Released Parties") from and against any and all actions, causes of action, suits, claims, demands, liabilities, losses, costs, damages,
 awards, penalties, fines, interest and expenses, of any kind or character, asserted against, resulting to, imposed upon or incurred by the Released Parties, directly or 
indirectly, in any way related to, by reason of, based upon or resulting from and injury, illness, disability or death, howsoever caused or arising, sustained in connecti
on with, arising out of, directly or indirectly resulting from or in any way connected with any Red Tide of NYC, Inc. practice, competition, event or activity.</p>

            <p>THE PROVISIONS OF THIS RELEASE FROM LIABILITY WAIVER SHALL APPLY EVENIF ANY INJURY, ILLNESS, DISABILITY OR DEATH IS CAUSED, IN WHOLE OR IN PART, BY THE SOL
E, JOINT OR CONCURRENT NEGLIGENCE, STRICT LIABILITY, CONTRACTUAL LIABILITY TO THIRD PARTIES, OR OTHER FAULT, WHETHER PASSIVE OR ACTIVE, OF ANY PERSON OR ENTITY, INCLUDING
, BUT NOT LIMITED TO, THE RELEASED PARTIES.</p>

            <p>The provisions of this Release from Liability Waiver shall inure to the benefit of the Released Parties, their respective heirs, legatees, beneficiaries, e
xecutors, administrators, legal representatives, successors and assigns.</p>

            <p>By submitting this registration form, you are agreeing to the terms of the "Release from Liability."</p>',0,'flatpages/faq.html',0,'text/html');
COMMIT;
