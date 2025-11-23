from manim import *import numpy as np

class CombinedVideo(Scene):
    """
    Physics Fundamentals
    Multi-scene video with 13 parts
    
    Total Duration: 105.0 seconds
    Number of Scenes: 13
    """
    
    def construct(self):
        """Main video construction with multiple scenes."""
        # Title card
        title = Text("Physics Fundamentals", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Play all scenes in sequence
        self.scene_1()
        self.scene_2()
        self.scene_3()
        self.scene_4()
        self.scene_5()
        self.scene_6()
        self.scene_7()
        self.scene_8()
        self.scene_9()
        self.scene_10()
        self.scene_11()
        self.scene_12()
        self.scene_13()
        
        # End card
        end_text = Text("End", font_size=36)
        self.play(FadeIn(end_text))
        self.wait(1)

    def scene_1(self):
        """Scene 1: Introduction to Classical Mechanics"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                title_classical_mechanics = Text("Classical Mechanics")
                title_classical_mechanics.move_to([0, 2.5, 0])
                title_classical_mechanics.set_color(WHITE)
                title_classical_mechanics.set_font_size(1.5)
                title_classical_mechanics.set_opacity(1.0)

                text_describes_motion = Text("describes the motion of objects")
                text_describes_motion.move_to([0, 1.0, 0])
                text_describes_motion.set_color(WHITE)
                text_describes_motion.set_font_size(0.8)
                text_describes_motion.set_opacity(1.0)

                text_examples = Text("from projectiles to parts of machinery, and astronomical objects like spacecraft, planets, stars, and galaxies.")
                text_examples.move_to([0, -0.5, 0])
                text_examples.set_color(WHITE)
                text_examples.set_font_size(0.7)
                text_examples.set_opacity(1.0)

                text_newtons_laws = Text("Newton's laws of motion form the foundation of classical mechanics.")
                text_newtons_laws.move_to([0, -2.5, 0])
                text_newtons_laws.set_color(YELLOW)
                text_newtons_laws.set_font_size(0.8)
                text_newtons_laws.set_opacity(1.0)

                # Animation Timeline:
                # 0.0s: anim_fade_in_title (FadeIn title_classical_mechanics, duration 1.0s)
                # 0.5s: anim_write_describes_motion (Write text_describes_motion, duration 1.5s)
                # 2.0s: anim_write_examples (Write text_examples, duration 2.5s)
                # 4.5s: anim_write_newtons_laws (Write text_newtons_laws, duration 2.0s)

                # Animate with proper timing
                # Animations starting at 0.0s and 0.5s (overlapping)
                self.play(
                    FadeIn(title_classical_mechanics, run_time=1.0),
                    Write(text_describes_motion, run_time=1.5).set_delay(0.5)
                )
                # This play call finishes at 2.0 seconds (max(1.0, 0.5+1.5))

                # Animation starting at 2.0s
                self.play(
                    Write(text_examples, run_time=2.5)
                )
                # This play call finishes at 2.0 + 2.5 = 4.5 seconds

                # Animation starting at 4.5s
                self.play(
                    Write(text_newtons_laws, run_time=2.0)
                )
                # This play call finishes at 4.5 + 2.0 = 6.5 seconds

                self.wait(7.0 - 6.5)
        
        # Scene transition
        self.wait(0.5)
    def scene_2(self):
        """Scene 2: Newton's First Law of Motion"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                # Create objects
                scene_title = Text(
                    "Newton's First Law of Motion",
                    font_size=0.8 * 15,  # Manim's default font_size is 0.5, so 0.8 * 0.5 = 0.4 relative to default.
                                         # Text uses font_size in points, so 0.8 * DEFAULT_FONT_SIZE (48) = 38.4.
                                         # A common way to scale is to use .scale() or specify font_size directly.
                                         # Let's use .scale() for clarity based on typical Manim usage for size.
                ).set_color(YELLOW).move_to([0, 3, 0])
                scene_title.scale(0.8) # Adjusting scale based on typical Manim text sizing.

                law_text = Text(
                    "The first law states that an object at rest stays at rest and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.",
                    font_size=0.6 * 15, # Similar scaling logic as above.
                    line_spacing=1.5, # Add line spacing for better readability of long text
                    # max_width=FRAME_WIDTH - 2 # Constrain width to prevent overflow
                ).set_color(WHITE).move_to([0, 0, 0])
                law_text.scale(0.6) # Adjusting scale. For long text, it's often better to set max_width.
                                    # Let's ensure it fits the screen.
                law_text.set_width(FRAME_WIDTH - 2) # Ensure text fits within screen width, with some padding.
                law_text.move_to([0,0,0]) # Re-center after setting width.

                # Animation Timeline:
                # 0.0s - 1.0s: FadeIn scene_title
                # 1.0s - 6.0s: Write law_text (starts after title fade-in finishes)
                # 6.0s - 8.0s: Wait

                # anim_title_fade_in
                self.play(FadeIn(scene_title), run_time=1.0)

                # anim_law_write
                self.play(Write(law_text), run_time=5.0)

                self.wait(8.0 - (1.0 + 5.0)) # Total duration 8.0s - (title_fade_in_duration + law_write_duration)
        
        # Scene transition
        self.wait(0.5)
    def scene_3(self):
        """Scene 3: Newton's Second Law of Motion: F=ma"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                # Create objects
                formula_f_ma = MathTex(r"F=ma")
                formula_f_ma.move_to([0, 0.5, 0])
                formula_f_ma.set_color(YELLOW)
                formula_f_ma.set_opacity(0.0)

                explanation_text = Text("Newton's Second Law of Motion")
                explanation_text.move_to([0, -0.5, 0])
                explanation_text.set_color(GRAY)
                explanation_text.set_opacity(0.0)
        
                # Animate with proper timing
                self.play(Write(formula_f_ma), run_time=2.0)
                self.play(FadeIn(explanation_text), run_time=1.5)
                self.wait(1.5) # Total scene duration is 5.0s (2.0s + 1.5s = 3.5s, remaining 1.5s)
        
        # Scene transition
        self.wait(0.5)
    def scene_4(self):
        """Scene 4: Newton's Third Law of Motion"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                newtons_third_law_text = Text(
                    "The third law states that for every action, there is an equal and opposite reaction.",
                    font_size=0.8 * DEFAULT_FONT_SIZE, # Scale font_size by 0.8
                    color=WHITE,
                    opacity=1.0
                )
                newtons_third_law_text.move_to([0, 0, 0])

                # Animate with proper timing
                # Delay before the first animation
                self.wait(0.5)

                # Animation: write_third_law
                self.play(Write(newtons_third_law_text), run_time=3.0)

                self.wait(1.5)
        
        # Scene transition
        self.wait(0.5)
    def scene_5(self):
        """Scene 5: Introduction to Thermodynamics"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                series_title = Text(
                    "Introduction to Thermodynamics",
                    color=WHITE,
                    font_size=1.0 * EM
                )
                series_title.move_to([0, 3.5, 0])

                thermodynamics_definition = Text(
                    "Thermodynamics is the branch of physics\n"
                    "that deals with heat and temperature,\n"
                    "and their relation to energy, work, radiation,\n"
                    "and properties of matter.",
                    color=WHITE,
                    font_size=0.7 * EM,
                    line_spacing=1.2
                )
                thermodynamics_definition.move_to([0, -0.5, 0])

                # Animate with proper timing
                # anim_write_series_title (start_time: 0.0, duration: 1.5)
                self.play(Write(series_title), run_time=1.5)

                # anim_write_definition (start_time: 1.5, duration: 3.5)
                # This animation starts immediately after the previous one finishes.
                self.play(Write(thermodynamics_definition), run_time=3.5)

                # Total animation time: 1.5 + 3.5 = 5.0 seconds
                # Remaining wait time: 6.0 - 5.0 = 1.0 second
                self.wait(1.0)
        
        # Scene transition
        self.wait(0.5)
    def scene_6(self):
        """Scene 6: First Law of Thermodynamics: Conservation of Energy"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                title_main = Text("First Law of Thermodynamics").scale(1.2).move_to([0, 3.0, 0]).set_color(WHITE)
                title_sub = Text("Conservation of Energy").scale(0.9).move_to([0, 2.0, 0]).set_color(YELLOW)
                statement_part1 = Text("Energy cannot be created or destroyed,").scale(0.7).move_to([0, 0.5, 0]).set_color(WHITE)
                statement_part2 = Text("only transferred or changed from one form to another.").scale(0.7).move_to([0, -0.5, 0]).set_color(WHITE)
                statement_alias = Text("This is also known as the conservation of energy.").scale(0.8).move_to([0, -2.0, 0]).set_color(GREEN)

                # Map object IDs to Manim objects for easier access
                obj_map = {
                    "title_main": title_main,
                    "title_sub": title_sub,
                    "statement_part1": statement_part1,
                    "statement_part2": statement_part2,
                    "statement_alias": statement_alias
                }

                # Animation Timeline processing
                animation_timeline = [
                    {"start_time": 0.3, "animation_id": "anim_title_sub", "animation_type": "write", "targets": ["title_sub"], "duration": 0.8},
                    {"start_time": 0.3, "animation_id": "anim_statement_part2", "animation_type": "write", "targets": ["statement_part2"], "duration": 1.5},
                    {"start_time": 0.5, "animation_id": "anim_title_main", "animation_type": "write", "targets": ["title_main"], "duration": 1.0},
                    {"start_time": 0.7, "animation_id": "anim_statement_part1", "animation_type": "write", "targets": ["statement_part1"], "duration": 1.5},
                    {"start_time": 0.7, "animation_id": "anim_statement_alias", "animation_type": "write", "targets": ["statement_alias"], "duration": 1.5}
                ]

                # Group animations by their start_time
                grouped_animations = {}
                for anim_data in animation_timeline:
                    start_time = anim_data['start_time']
                    if start_time not in grouped_animations:
                        grouped_animations[start_time] = []
                    grouped_animations[start_time].append(anim_data)

                sorted_start_times = sorted(grouped_animations.keys())

                current_scene_time = 0.0
                total_scene_duration = 10.0

                for start_time in sorted_start_times:
                    # Calculate wait duration to reach the next group's start_time
                    wait_duration = start_time - current_scene_time
                    if wait_duration > 0:
                        self.wait(wait_duration)
                        current_scene_time += wait_duration
                    # If wait_duration is negative, it means this group's intended start_time
                    # is before the previous self.play call finished.
                    # In this simplified model, it will effectively start immediately after
                    # the previous self.play finishes, potentially delaying it from the
                    # exact timeline start_time. current_scene_time remains unchanged if wait_duration <= 0.

                    animations_to_play_in_group = []
                    max_group_run_time = 0.0

                    for anim_data in grouped_animations[start_time]:
                        obj = obj_map[anim_data['targets'][0]]
                        anim_type = anim_data['animation_type']
                        duration = anim_data['duration']

                        manim_anim = None
                        if anim_type == "write":
                            manim_anim = Write(obj, run_time=duration)
                        elif anim_type == "create":
                            manim_anim = Create(obj, run_time=duration)
                        elif anim_type == "fade_in":
                            manim_anim = FadeIn(obj, run_time=duration)
                        elif anim_type == "fade_out":
                            manim_anim = FadeOut(obj, run_time=duration)
                        elif anim_type == "transform":
                            from_obj = obj_map[anim_data['from_object']]
                            to_obj = obj_map[anim_data['to_object']]
                            manim_anim = Transform(from_obj, to_obj, run_time=duration)
                        elif anim_type == "move_to":
                            # For .animate, run_time is passed to the animate method
                            manim_anim = obj.animate(run_time=duration).move_to(anim_data['target_position'])
                        elif anim_type == "shift":
                            manim_anim = obj.animate(run_time=duration).shift(anim_data['offset'])
                        elif anim_type == "rotate":
                            manim_anim = obj.animate(run_time=duration).rotate(anim_data['angle'])
                        elif anim_type == "scale":
                            manim_anim = obj.animate(run_time=duration).scale(anim_data['factor'])
                
                        if manim_anim:
                            animations_to_play_in_group.append(manim_anim)
                            max_group_run_time = max(max_group_run_time, duration)

                    if animations_to_play_in_group:
                        # self.play will automatically use the longest run_time among its animations
                        self.play(*animations_to_play_in_group)
                        current_scene_time += max_group_run_time

                # Final wait to ensure the scene reaches its total specified duration
                remaining_time = total_scene_duration - current_scene_time
                if remaining_time > 0:
                    self.wait(remaining_time)
        
        # Scene transition
        self.wait(0.5)
    def scene_7(self):
        """Scene 7: Second Law of Thermodynamics: Entropy"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                scene_title = Text("Second Law of Thermodynamics: Entropy")
                scene_title.move_to([0, 3.5, 0])
                scene_title.set_color(WHITE)
                scene_title.set_font_size(0.8 * DEFAULT_FONT_SIZE)

                concept_text = Text("The second law introduces the concept of entropy, stating that the entropy of an isolated system never decreases.")
                concept_text.move_to([0, 2.0, 0])
                concept_text.set_color(WHITE)
                concept_text.set_font_size(0.6 * DEFAULT_FONT_SIZE)

                example_text = Text("Heat flows naturally from hot to cold objects, and it takes work to move heat from cold to hot.")
                example_text.move_to([0, 0.5, 0])
                example_text.set_color(WHITE)
                example_text.set_font_size(0.5 * DEFAULT_FONT_SIZE)

                work_label = Text("Work")
                work_label.move_to([0, -3.2, 0])
                work_label.set_color(YELLOW)
                work_label.set_font_size(0.4 * DEFAULT_FONT_SIZE)

                hot_object = Circle(radius=0.7)
                hot_object.move_to([-3, -2.5, 0])
                hot_object.set_color(RED)
                hot_object.set_fill(RED, opacity=0.8)

                cold_object = Circle(radius=0.7)
                cold_object.move_to([3, -2.5, 0])
                cold_object.set_color(BLUE)
                cold_object.set_fill(BLUE, opacity=0.8)

                # Define arrows after objects are positioned
                # Natural heat flow: Hot (left) to Cold (right)
                natural_heat_arrow = Arrow(
                    start=hot_object.get_right(),
                    end=cold_object.get_left(),
                    buff=0.1 # Small buffer so arrow doesn't touch circle
                )
                natural_heat_arrow.set_color(ORANGE)

                # Work heat flow: Cold (right) to Hot (left), shifted down
                work_heat_arrow = Arrow(
                    start=cold_object.get_left() + DOWN * 0.5, # From cold object's left, shifted down
                    end=hot_object.get_right() + DOWN * 0.5,   # To hot object's right, shifted down
                    buff=0.1
                )
                work_heat_arrow.set_color(YELLOW)

                # Animations
                # anim_title_write (0.0s - 2.0s)
                self.play(Write(scene_title), run_time=2.0)

                # anim_concept_write (2.0s - 6.0s)
                self.play(Write(concept_text), run_time=4.0)

                # anim_example_write (6.0s - 10.0s)
                self.play(Write(example_text), run_time=4.0)

                # anim_objects_create (10.0s - 11.0s)
                self.play(Create(VGroup(hot_object, cold_object)), run_time=1.0)

                # anim_natural_arrow_show (11.0s - 12.5s)
                self.play(Create(natural_heat_arrow), run_time=1.5)

                # Wait to align with anim_work_flow start time (13.0s)
                # Current time is 12.5s, need to wait 0.5s
                self.wait(0.5)

                # anim_work_flow (13.0s - 14.5s) and anim_work_label_fade_in (13.5s - 14.0s)
                # Use LaggedStart to start FadeIn(work_label) 0.5s after Create(work_heat_arrow)
                self.play(
                    LaggedStart(
                        Create(work_heat_arrow, run_time=1.5),
                        FadeIn(work_label, run_time=0.5),
                        lag_ratio=0.5 / 1.5 # FadeIn starts 0.5s into the 1.5s duration of Create
                    )
                )

                # The last animation group finished at 13.0s + 1.5s = 14.5s
                self.wait(15.0 - 14.5)
        
        # Scene transition
        self.wait(0.5)
    def scene_8(self):
        """Scene 8: Introduction to Electromagnetism"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                title_em = Text("Electromagnetism", font_size=1.5 * 40).move_to([0, 3.5, 0]).set_color(BLUE)
                def_text_part1 = Text("is a branch of physics involving\nthe study of the", font_size=1.0 * 40).move_to([0, 2.0, 0]).set_color(WHITE)
                em_force_keyword_1 = Text("Electromagnetic Force,", font_size=1.0 * 40).move_to([0, 0.5, 0]).set_color(YELLOW)
                interaction_text = Text("a type of physical interaction that occurs\nbetween electrically charged particles.", font_size=1.0 * 40).move_to([0, -0.5, 0]).set_color(WHITE)
                carrier_text_part1 = Text("The", font_size=1.0 * 40).move_to([-5.0, -2.0, 0]).set_color(WHITE)
                em_force_keyword_2 = Text("electromagnetic force", font_size=1.0 * 40).move_to([-2.0, -2.0, 0]).set_color(YELLOW)
                carrier_text_part2 = Text(" is carried by ", font_size=1.0 * 40).move_to([1.0, -2.0, 0]).set_color(WHITE)
                em_fields_keyword = Text("electromagnetic fields", font_size=1.0 * 40).move_to([4.0, -2.0, 0]).set_color(YELLOW)
                composed_text_part1 = Text("composed of ", font_size=1.0 * 40).move_to([-4.0, -3.0, 0]).set_color(WHITE)
                electric_fields_keyword = Text("electric fields", font_size=1.0 * 40).move_to([-1.5, -3.0, 0]).set_color(YELLOW)
                and_text = Text("and", font_size=1.0 * 40).move_to([0.5, -3.0, 0]).set_color(WHITE)
                magnetic_fields_keyword = Text("magnetic fields,", font_size=1.0 * 40).move_to([2.5, -3.0, 0]).set_color(YELLOW)
                radiation_text_part1 = Text("and it is responsible for ", font_size=1.0 * 40).move_to([-3.0, -4.0, 0]).set_color(WHITE)
                em_radiation_keyword = Text("electromagnetic radiation", font_size=1.0 * 40).move_to([1.0, -4.0, 0]).set_color(YELLOW)
                such_as_text = Text(" such as ", font_size=1.0 * 40).move_to([3.5, -4.0, 0]).set_color(WHITE)
                light_keyword = Text("light.", font_size=1.0 * 40).move_to([5.0, -4.0, 0]).set_color(YELLOW)

                # Store objects in a dictionary for easy access by ID
                mobjects = {
                    "title_em": title_em,
                    "def_text_part1": def_text_part1,
                    "em_force_keyword_1": em_force_keyword_1,
                    "interaction_text": interaction_text,
                    "carrier_text_part1": carrier_text_part1,
                    "em_force_keyword_2": em_force_keyword_2,
                    "carrier_text_part2": carrier_text_part2,
                    "em_fields_keyword": em_fields_keyword,
                    "composed_text_part1": composed_text_part1,
                    "electric_fields_keyword": electric_fields_keyword,
                    "and_text": and_text,
                    "magnetic_fields_keyword": magnetic_fields_keyword,
                    "radiation_text_part1": radiation_text_part1,
                    "em_radiation_keyword": em_radiation_keyword,
                    "such_as_text": such_as_text,
                    "light_keyword": light_keyword,
                }

                # Animation timeline data
                animations_timeline = [
                    {"start_time": 0.0, "animation_id": "anim_title_fade_in", "animation_type": "fade_in", "targets": ["title_em"], "duration": 1.0},
                    {"start_time": 0.1, "animation_id": "anim_em_force_keyword_1_write", "animation_type": "write", "targets": ["em_force_keyword_1"], "duration": 0.7},
                    {"start_time": 0.1, "animation_id": "anim_interaction_text_write", "animation_type": "write", "targets": ["interaction_text"], "duration": 1.5},
                    {"start_time": 0.1, "animation_id": "anim_em_force_keyword_2_write", "animation_type": "write", "targets": ["em_force_keyword_2"], "duration": 0.7},
                    {"start_time": 0.1, "animation_id": "anim_carrier_part2_write", "animation_type": "write", "targets": ["carrier_text_part2"], "duration": 0.7},
                    {"start_time": 0.1, "animation_id": "anim_em_fields_keyword_write", "animation_type": "write", "targets": ["em_fields_keyword"], "duration": 0.8},
                    {"start_time": 0.1, "animation_id": "anim_electric_fields_keyword_write", "animation_type": "write", "targets": ["electric_fields_keyword"], "duration": 0.7},
                    {"start_time": 0.1, "animation_id": "anim_and_text_write", "animation_type": "write", "targets": ["and_text"], "duration": 0.2},
                    {"start_time": 0.1, "animation_id": "anim_magnetic_fields_keyword_write", "animation_type": "write", "targets": ["magnetic_fields_keyword"], "duration": 0.7},
                    {"start_time": 0.1, "animation_id": "anim_em_radiation_keyword_write", "animation_type": "write", "targets": ["em_radiation_keyword"], "duration": 1.0},
                    {"start_time": 0.1, "animation_id": "anim_such_as_text_write", "animation_type": "write", "targets": ["such_as_text"], "duration": 0.4},
                    {"start_time": 0.1, "animation_id": "anim_light_keyword_write", "animation_type": "write", "targets": ["light_keyword"], "duration": 0.4},
                    {"start_time": 0.2, "animation_id": "anim_composed_part1_write", "animation_type": "write", "targets": ["composed_text_part1"], "duration": 0.5},
                    {"start_time": 0.3, "animation_id": "anim_carrier_part1_write", "animation_type": "write", "targets": ["carrier_text_part1"], "duration": 0.4},
                    {"start_time": 0.3, "animation_id": "anim_radiation_part1_write", "animation_type": "write", "targets": ["radiation_text_part1"], "duration": 1.0},
                    {"start_time": 0.5, "animation_id": "anim_def_part1_write", "animation_type": "write", "targets": ["def_text_part1"], "duration": 1.0}
                ]

                # Group animations by start_time
                from collections import defaultdict
                animations_by_start_time = defaultdict(list)
                for anim_data in animations_timeline:
                    animations_by_start_time[anim_data["start_time"]].append(anim_data)

                sorted_start_times = sorted(animations_by_start_time.keys())

                current_scene_time = 0.0
                scene_total_duration = 12.0

                for start_time in sorted_start_times:
                    # Wait until the current start_time
                    wait_duration = start_time - current_scene_time
                    if wait_duration > 0:
                        self.wait(wait_duration)
            
                    manim_animations_to_play = []
                    max_duration_for_group = 0.0
            
                    for anim_data in animations_by_start_time[start_time]:
                        target_mobjects = [mobjects[target_id] for target_id in anim_data["targets"]]
                
                        # Map animation type to Manim method
                        if anim_data["animation_type"] == "write":
                            manim_animations_to_play.extend([Write(obj) for obj in target_mobjects])
                        elif anim_data["animation_type"] == "create":
                            manim_animations_to_play.extend([Create(obj) for obj in target_mobjects])
                        elif anim_data["animation_type"] == "fade_in":
                            manim_animations_to_play.extend([FadeIn(obj) for obj in target_mobjects])
                        elif anim_data["animation_type"] == "fade_out":
                            manim_animations_to_play.extend([FadeOut(obj) for obj in target_mobjects])
                        # Add other animation types if needed, following the mapping
                
                        max_duration_for_group = max(max_duration_for_group, anim_data["duration"])
            
                    if manim_animations_to_play:
                        self.play(*manim_animations_to_play, run_time=max_duration_for_group)
                        current_scene_time = start_time + max_duration_for_group 
                    else:
                        # If no animations were added for some reason, just advance time by wait_duration
                        current_scene_time = start_time

                remaining_time = scene_total_duration - current_scene_time
                if remaining_time > 0:
                    self.wait(remaining_time)
                else:
                    self.wait(1.0) # Default wait if the scene somehow ran longer than expected or ended too quickly
        
        # Scene transition
        self.wait(0.5)
    def scene_9(self):
        """Scene 9: Electric and Magnetic Field Generation"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                scene_title = Text(
                    "Electric and Magnetic Field Generation",
                    font_size=0.8 * 15, # Manim's default font_size is 15, so 0.8 * 15
                    color=WHITE
                ).move_to([0, 3.5, 0])

                electric_field_text = Text(
                    "Electric fields are created by electric charges.",
                    font_size=0.6 * 15,
                    color=BLUE
                ).move_to([-3, 1, 0])

                magnetic_field_text = Text(
                    "Magnetic fields are created by moving charges (electric currents).",
                    font_size=0.6 * 15,
                    color=RED
                ).move_to([-3, -1, 0])

                # Animate
                # anim_title_fade_in (start_time: 0.0, duration: 1.0)
                self.play(FadeIn(scene_title), run_time=1.0)

                # anim_write_electric_field (start_time: 1.0, duration: 2.0)
                # This animation starts immediately after the previous one ends
                self.play(Write(electric_field_text), run_time=2.0)

                # anim_write_magnetic_field (start_time: 3.0, duration: 2.5)
                # This animation starts immediately after the previous one ends
                self.play(Write(magnetic_field_text), run_time=2.5)

                # Last animation ends at 3.0 + 2.5 = 5.5s
                # Remaining time: 6.0 - 5.5 = 0.5s
                self.wait(0.5)
        
        # Scene transition
        self.wait(0.5)
    def scene_10(self):
        """Scene 10: Maxwell's Equations"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                title_text = Text("Maxwell's Equations", color=WHITE).scale(1.2)
                title_text.move_to([0, 3, 0])

                description_text = Text(
                    "Maxwell's equations describe how electric and magnetic fields are generated and altered by each other and by charges and currents.",
                    color=WHITE,
                    font_size=0.8 * DEFAULT_FONT_SIZE
                ).set_opacity(1.0)
                description_text.move_to([0, -0.5, 0])

                # Animation Timeline
                # write_title (start_time: 0.5, duration: 1.5)
                self.wait(0.5)
                self.play(Write(title_text), run_time=1.5)

                # write_description (start_time: 2.0, duration: 3.0)
                # Current time is 0.5 + 1.5 = 2.0, which matches the start_time for the next animation.
                self.play(Write(description_text), run_time=3.0)

                # Last animation ends at 2.0 + 3.0 = 5.0s.
                self.wait(6.0 - 5.0)
        
        # Scene transition
        self.wait(0.5)
    def scene_11(self):
        """Scene 11: Introduction to Quantum Mechanics"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                scene_title = Text(
                    "Introduction to Quantum Mechanics",
                    font_size=0.8,
                    color=YELLOW
                ).move_to([0, 3, 0])

                qm_definition_part1 = Text(
                    "Quantum mechanics is a fundamental theory in physics that provides a description of the physical properties of nature",
                    font_size=0.6,
                    color=WHITE,
                    disable_ligatures=True
                ).move_to([0, 1, 0]).set_width(FRAME_WIDTH - 1) # Adjust width for text wrapping

                qm_definition_part2 = Text(
                    "at the scale of atoms and subatomic particles.",
                    font_size=0.6,
                    color=WHITE,
                    disable_ligatures=True
                ).move_to([0, 0, 0]).set_width(FRAME_WIDTH - 1) # Adjust width for text wrapping

                qm_explanation = Text(
                    "It explains phenomena that classical physics cannot, such as wave-particle duality and quantum entanglement.",
                    font_size=0.6,
                    color=WHITE,
                    disable_ligatures=True
                ).move_to([0, -2, 0]).set_width(FRAME_WIDTH - 1) # Adjust width for text wrapping

                # Animate with proper timing based on the Animation Timeline
                # The 'begin' parameter of an animation specifies its start time relative
                # to the start of the self.play call.
                # The overall run_time of the self.play call is determined by the latest
                # ending animation.

                # Calculate end times for each animation:
                # qm_definition_part2: starts 0.2s, duration 1.5s -> ends 1.7s
                # scene_title:         starts 0.5s, duration 1.5s -> ends 2.0s
                # qm_definition_part1: starts 0.5s, duration 2.5s -> ends 3.0s
                # qm_explanation:      starts 0.5s, duration 3.0s -> ends 3.5s
                # The latest end time is 3.5s, so the self.play call will have run_time=3.5.

                self.play(
                    Write(qm_definition_part2, run_time=1.5, begin=0.2),
                    Write(scene_title, run_time=1.5, begin=0.5),
                    Write(qm_definition_part1, run_time=2.5, begin=0.5),
                    Write(qm_explanation, run_time=3.0, begin=0.5),
                    run_time=3.5 # Total duration for this play call
                )

                # The animations above conclude at 3.5s.
                self.wait(10.0 - 3.5)
        
        # Scene transition
        self.wait(0.5)
    def scene_12(self):
        """Scene 12: Heisenberg's Uncertainty Principle"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                title_text = Text("Heisenberg's Uncertainty Principle")
                title_text.move_to([0, 3, 0])
                title_text.set_color(WHITE)
                title_text.set_opacity(1.0)
                title_text.set_height(1.0) # Interpreting 'size: 1.0' as setting height to 1 Manim unit

                principle_intro_text = Text("The uncertainty principle, formulated by Werner Heisenberg, states that")
                principle_intro_text.move_to([0, 1, 0])
                principle_intro_text.set_color(LIGHT_GRAY)
                principle_intro_text.set_opacity(1.0)
                principle_intro_text.set_height(1.0)

                position_part_text = Text("the more precisely the POSITION of a particle is determined,")
                position_part_text.move_to([0, 0, 0])
                position_part_text.set_color(BLUE)
                position_part_text.set_opacity(1.0)
                position_part_text.set_height(1.0)

                momentum_part_text = Text("the less precisely its MOMENTUM can be known,")
                momentum_part_text.move_to([0, -1, 0])
                momentum_part_text.set_color(RED)
                momentum_part_text.set_opacity(1.0)
                momentum_part_text.set_height(1.0)

                vice_versa_text = Text("and vice versa.")
                vice_versa_text.move_to([0, -2, 0])
                vice_versa_text.set_color(LIGHT_GRAY)
                vice_versa_text.set_opacity(1.0)
                vice_versa_text.set_height(1.0)

                # Animate with proper timing
                # anim_title_create (delay: 0.0, duration: 1.0)
                self.play(Create(title_text), run_time=1.0)

                # Delay before the next set of animations (0.5s)
                self.wait(0.5)

                # anim_intro_write, anim_position_write, anim_momentum_write, anim_vice_versa_write
                # All start simultaneously after the delay.
                # Durations: 1.5, 1.5, 1.5, 1.0. The self.play block will run for the maximum duration (1.5s).
                self.play(
                    Write(principle_intro_text, run_time=1.5),
                    Write(position_part_text, run_time=1.5),
                    Write(momentum_part_text, run_time=1.5),
                    Write(vice_versa_text, run_time=1.0)
                )

                # Calculate remaining time for the scene's total duration (10.0s)
                # Elapsed time: 1.0s (title create) + 0.5s (wait) + 1.5s (parallel writes) = 3.0s
                # Remaining wait time: 10.0s - 3.0s = 7.0s
                self.wait(7.0)
        
        # Scene transition
        self.wait(0.5)
    def scene_13(self):
        """Scene 13: Schrödinger's Equation"""
        # Clear previous scene
        self.clear()
        
        # Scene content
                self.camera.background_color = BLACK

                # Create objects
                part_info_text = Text(
                    "Part 13 of 13",
                    font_size=1.0 * 24, # Manim's default font_size is 48, so 1.0 * 24 makes it half the default
                    color=GRAY
                )
                part_info_text.move_to([0, 3.5, 0])

                title_text = Text(
                    "Schrödinger's Equation",
                    font_size=1.0 * 48, # Manim's default font_size is 48
                    color=BLUE
                )
                title_text.move_to([0, 2, 0])

                definition_text = Text(
                    "Schrödinger's equation is the fundamental equation of quantum mechanics\nthat describes how the quantum state of a physical system changes over time.",
                    font_size=1.0 * 24, # Manim's default font_size is 48, so 1.0 * 24 makes it half the default
                    color=WHITE,
                    line_spacing=1.5 # Adjust line spacing for multiline text
                )
                definition_text.move_to([0, -0.5, 0])

                # Animate with proper timing
                # Animation: fade_in_part_info (start_time: 0.0, duration: 0.5)
                self.play(FadeIn(part_info_text), run_time=0.5)

                # Animation: fade_in_title (start_time: 0.5, duration: 1.0)
                self.play(FadeIn(title_text), run_time=1.0)

                # Animation: write_definition (start_time: 1.5, duration: 3.0)
                self.play(Write(definition_text), run_time=3.0)

                self.wait(0.5)
        
        # Scene transition
        self.wait(0.5)