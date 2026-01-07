import os
import json
import numpy as np

def get_number_events_from_file(file_path, targets_id):
    ret = 0
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        if 'events' not in data or not data['events']:
            return ret

        for entry in data['events']:
            s_pos = entry['start_frame']
            f_pos = entry['end_frame']
            event_id = entry['type']

            if event_id in targets_id:
                if f_pos - s_pos >= 1:
                    ret += 1

        return ret

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0


def get_positions_from_file_exclusive(file_path, targets_id, offset=20):
    # Exclusive events only containing target IDs, and strictly isolated from any other events
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        if 'events' not in data or not data['events']:
            return [], None

        video_id = data.get('video_id')

        all_event_frames = set()
        target_event_frames = {}

        sorted_events = sorted(
            data['events'], key=lambda x: x['start_frame']
        )

        # Register frame-level occupancy
        for entry in sorted_events:
            s_pos = entry['start_frame']
            f_pos = entry['end_frame']
            event_id = entry['type']

            for frame in range(s_pos, f_pos + 1):
                all_event_frames.add(frame)

                if event_id in targets_id:
                    if frame not in target_event_frames:
                        target_event_frames[frame] = set()
                    target_event_frames[frame].add(event_id)

        # Identify exclusive ranges
        exclusive_ranges = []
        current_range = None

        for entry in sorted_events:
            s_pos = entry['start_frame']
            f_pos = entry['end_frame']
            event_id = entry['type']

            if event_id in targets_id and (f_pos - s_pos >= 1):

                is_exclusive = all(
                    target_event_frames.get(f, set()).issubset(set(targets_id))
                    for f in range(s_pos, f_pos + 1)
                )

                if is_exclusive:
                    if current_range and current_range[1] == s_pos - 1:
                        current_range = (current_range[0], f_pos)
                    else:
                        if current_range:
                            exclusive_ranges.append(current_range)
                        current_range = (s_pos, f_pos)

        if current_range:
            exclusive_ranges.append(current_range)

        # Strict isolation (pre-event buffer)
        final_cases = []
        for s_curr, f_curr in exclusive_ranges:
            buffer_start = s_curr - offset
            buffer_end = s_curr - 1

            is_isolated = True
            for frame in range(buffer_start, buffer_end + 1):
                if frame in all_event_frames:
                    is_isolated = False
                    break

            if is_isolated:
                final_cases.append((s_curr, f_curr))

        return final_cases, video_id

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return [], None
    
def get_positions_from_file(file_path, targets_id, offset=20):
    # Events only containing target IDs, and strictly isolated from any identical events (events with the same ID)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        if 'events' not in data or not data['events']:
            return [], None

        anchors = data.get('anchors', [0])

        frame_events = {}

        for entry in data['events']:
            s_pos = entry['start_frame']
            f_pos = entry['end_frame']
            event_id = entry['type']

            for frame in range(s_pos, f_pos + 1):
                frame_events.setdefault(frame, set()).add(event_id)

        exclusive_ranges = []
        current_range = None

        for entry in data['events']:
            s_pos = entry['start_frame']
            f_pos = entry['end_frame']
            event_id = entry['type']

            if event_id in targets_id:
                if s_pos > anchors[0] and (f_pos - s_pos >= 1):
                    if all(
                        frame_events[frame].issubset(set(targets_id))
                        for frame in range(s_pos, f_pos + 1)
                    ):
                        if current_range and current_range[1] == s_pos - 1:
                            current_range = (current_range[0], f_pos)
                        else:
                            if current_range:
                                exclusive_ranges.append(current_range)
                            current_range = (s_pos, f_pos)

        if current_range:
            exclusive_ranges.append(current_range)

        cases_ret = []
        for i, rng in enumerate(exclusive_ranges):
            if i == 0:
                cases_ret.append(rng)
            else:
                if rng[0] - exclusive_ranges[i - 1][1] >= offset:
                    cases_ret.append(rng)

        return cases_ret, data.get('video_id')

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return [], None


if __name__ == "__main__":
    analise_validation_events = False # Set to True to analyse validation events, False for test events
    offset = 20 # frames apart to consider events isolated (10 before and 10 after, like in the paper)

    ##### Define event to analise #####

    # event_title = 'InstOcc'
    # event_id = ['i_o', 'n_o']
    # event_title = 'otherOcc'
    # event_id = ['o_o', 'g_o']
    # event_title = 'OrganOcc'
    # event_id = ['o_o']
    # event_title = 'AllOcc'
    # event_id = ['i_o', 'n_o', 'g_o', 'o_o']
    # event_title = 'Fast'
    # event_id = ['f']
    # event_title = 'OutFrame'
    # event_id = ['o_f']
    event_title = 'Deformation'
    event_id = ['d']
    ##################################

    # paths to case event files
    val_case_details_files = [
        'annotations/Validation/case_1_1_events.json',
        'annotations/Validation/case_1_2_events.json',
        'annotations/Validation/case_1_3_events.json',
        'annotations/Validation/case_2_1_events.json',
        'annotations/Validation/case_2_2_events.json',
        'annotations/Validation/case_2_3_events.json',
        'annotations/Validation/case_2_4_events.json',
        'annotations/Validation/case_3_1_events.json',
        'annotations/Validation/case_3_2_events.json',
        'annotations/Validation/case_3_3_events.json',
        'annotations/Validation/case_3_4_events.json']
    test_case_details_files = [
        'annotations/Test/case_1_1_events.json',
        'annotations/Test/case_1_2_events.json',
        'annotations/Test/case_1_3_events.json',
        'annotations/Test/case_2_1_events.json',
        'annotations/Test/case_2_2_events.json',
        'annotations/Test/case_2_3_events.json',
        'annotations/Test/case_2_4_events.json',
        'annotations/Test/case_3_1_events.json',
        'annotations/Test/case_3_2_events.json',
        'annotations/Test/case_3_3_events.json',
        'annotations/Test/case_3_4_events.json',
        'annotations/Test/case_4_1_events.json',
        'annotations/Test/case_4_2_events.json',
        'annotations/Test/case_4_3_events.json',
        'annotations/Test/case_4_4_events.json',
        'annotations/Test/case_5_1_events.json',
        'annotations/Test/case_5_2_events.json',
        'annotations/Test/case_5_3_events.json',
        'annotations/Test/case_5_4_events.json']

    ############################ Count total number of events ####################################
    event_number = 0
    clip_number = 0
    if analise_validation_events:
        case_details_files = val_case_details_files
    else:
        case_details_files = test_case_details_files

    for case_detail_file in case_details_files:
        clip_num_events = get_number_events_from_file(case_detail_file, event_id)
        print(f'{os.path.basename(case_detail_file).split("_")[1]}_{os.path.basename(case_detail_file).split("_")[2]}: {clip_num_events}')
        event_number = event_number + clip_num_events
        if clip_num_events > 0:
            clip_number += 1
    print(f'[{event_title}] The event {event_id}, the number of events was: {event_number} in {clip_number} clips')

    ################################## Analise events in isolation ####################################################
    # Get all events details
    cases_events_list = []
    event_list = []
    for case_detail_file in case_details_files:
        _event_pos, video_id = get_positions_from_file(
            case_detail_file, event_id, offset)
        if _event_pos is not None:
            _case_events_frame_ranges = []
            for event_pos in _event_pos:
                #remove the events that start with frame 0, since we dont have frames without the event to calculate the baseline error
                if event_pos[0] == 0:
                    continue
                else:
                    event_list.append([event_pos, video_id, event_pos[1]-event_pos[0]])
                    _case_events_frame_ranges.append(
                        [event_pos[0]-offset//2, event_pos[1]+offset//2])
            cases_events_list.append(
                [video_id, _case_events_frame_ranges])

    event_len = [event[2] for event in event_list]
    event_len_array = np.array(event_len)
    mean_len = event_len_array.mean()
    std_len = event_len_array.std()
    min_len = event_len_array.min()
    max_len = event_len_array.max()
    print(f'[{event_title}] isolated events analised ({offset} frames apart) = {len(event_len)}; Avg len = {mean_len} +- {std_len}; min = {min_len}; max = {max_len}')